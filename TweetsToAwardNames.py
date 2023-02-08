import json
import re
import spacy
import nltk
#from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.metrics.distance import edit_distance
from nltk.corpus import wordnet
from datetime import datetime
from collections import defaultdict
from AwardCategory import AwardCategory
from utils import standardize, filter_dict, sort_dict_alpha, sort_dict_decreasing_count, dict_to_json

def is_award_topic(award_name):
    #! this is kind of sketch but i feel like we can defend it as being "domain knowledge"
    notMovieRelated = ["speech","outfit","look","insult","hair","dressed"]
    for nr in notMovieRelated:
        if nr in award_name:
            return False
    return True

def find_awards(tweets):
    uniqueAwards = defaultdict(int)

    seenTweets = set()
    for tweet in tweets:
        text = tweet['text'].lower()
        bestSearch = re.search(r"\s*(?P<award_name>[Bb]est .*) goes to",text)
        if bestSearch is not None and text not in seenTweets:
            seenTweets.add(text)
            uniqueAwards[bestSearch['award_name']] += 1

    ## get rid of awards with less than 2 occurrences
    uniqueAwards = filter_dict(uniqueAwards,minCount=2)
    ## reset counts to 0
    uniqueAwards = {k: 0 for k in uniqueAwards.keys()}
    ## sort dictionary by word length
    uniqueAwards = dict(sorted(uniqueAwards.items(), key= lambda x: -len(x[0].split())))

    seenTweets = set()
    for award in uniqueAwards:
        awardRegex = r"(\s*" + re.escape(award) + r".*)"
        for tweet in tweets:
            text = standardize(tweet['text']).lower()
            awardSearch = re.search(awardRegex,text)
            if awardSearch is not None and text not in seenTweets:
                seenTweets.add(text)
                uniqueAwards[award] += 1

    uniqueAwards = filter_dict(uniqueAwards,minCount=3)

    return {k: AwardCategory(k,v) for k, v in uniqueAwards.items() if is_award_topic(k)}

def merge_identical(d):
    with open("saved_jsons/clean_aliases.json", "r") as file:
        cleaned_award_names = json.load(file)

    new_d = dict()
    d = dict(sorted(d.items(), key= lambda x: -len(x[0].split())))
    set_to_name = {}

    for awardName, awardCategory in d.items():
        cleanedAwardName = cleaned_award_names[awardName]
        cleanedAwardNameWords = tuple(sorted(tuple(set(cleanedAwardName.split()))))
        set_to_name[cleanedAwardNameWords] = awardName
        if cleanedAwardNameWords not in new_d:
            new_d[cleanedAwardNameWords] = AwardCategory(awardName)
        # else:
            # print(f"merging {awardName} into {cleanedAwardName}")
        new_d[cleanedAwardNameWords].count += awardCategory.count
        new_d[cleanedAwardNameWords].aliases |= awardCategory.aliases
    new_d = {set_to_name[k]:v for k,v in new_d.items()}
    clean_aliases(new_d)
    return new_d

def merge_substrings(d):
    new_d = dict()
    d = dict(sorted(d.items(), key= lambda x: -len(x[0].split())))
    with open("saved_jsons/clean_aliases.json", "r") as file:
        cleaned_award_names = json.load(file)

    for awardName, awardCategory in d.items():
        merged = False
        substringOf = []
        substringOfValues = []
        for mergedName in new_d:
                for alias in new_d[mergedName].aliases:
                    if cleaned_award_names[awardName] in cleaned_award_names[alias]:
                        substringOf.append(mergedName)
                        substringOfValues.append(new_d[mergedName].count)
                        break

        if len(substringOf) == 1:
            new_d[substringOf[0]].count += awardCategory.count
            new_d[substringOf[0]].aliases |= awardCategory.aliases
            merged = True

        if not merged and len(substringOf) == 0:
            new_d[awardName] = awardCategory

    return new_d

def merge_simplify(d,simplify_dict):
    with open("saved_jsons/clean_aliases.json", "r") as file:
        cleaned_award_names = json.load(file)

    simplify_keys = simplify_dict.keys()

    new_d = dict()
    d = dict(sorted(d.items(), key= lambda x: -len(x[0].split())))
    set_to_name = {}

    for awardName, awardCategory in d.items():
        cleanedAwardName = cleaned_award_names[awardName]
        for key in simplify_keys:
            if key in cleanedAwardName:
                cleanedAwardName = cleanedAwardName.replace(key,simplify_dict[key])
        
        cleanedAwardNameWords = tuple(sorted(tuple(set(cleanedAwardName.split()))))
        set_to_name[cleanedAwardNameWords] = awardName
        if cleanedAwardNameWords not in new_d:
            new_d[cleanedAwardNameWords] = AwardCategory(awardName)
        # else:
            # print(f"merging {awardName} into {cleanedAwardName}")
        new_d[cleanedAwardNameWords].count += awardCategory.count
        new_d[cleanedAwardNameWords].aliases |= awardCategory.aliases
    new_d = {set_to_name[k]:v for k,v in new_d.items()}
    clean_aliases(new_d)
    return new_d

def add_short_versions(d):
    with open("saved_jsons/clean_aliases.json", "r") as file:
        cleaned_award_names = json.load(file)
    for name, award in d.items():
        curr_aliases = set(award.aliases)
        for alias in award.aliases:
            clean_award_name = cleaned_award_names[alias]
            if clean_award_name not in curr_aliases:
                curr_aliases.add(clean_award_name)
        d[name].aliases = list(curr_aliases)
    return d


def get_word_neighbors(d):
    with open("saved_jsons/clean_aliases.json", "r") as file:
        cleaned_award_names = json.load(file)

    word_neighbors = dict()

    for k in d.keys():
        cleaned_name = cleaned_award_names[k]
        split = cleaned_name[5:].split()
        for idx, word in enumerate(split):
            if word not in word_neighbors: 
                word_neighbors[word] = set()
            word_set = word_neighbors[word]

            if idx < len(split)-1:
                following_word = split[idx+1]
                if following_word not in ["or","and","in","for","to"]:
                    word_set.add(split[idx+1])
    for word in word_neighbors:
        word_neighbors[word] = list(word_neighbors[word])
    
    dict_to_json(word_neighbors,"word_neighbors",folderName="saved_jsons/")
    return word_neighbors

def get_simplification_dict(word_neighbors):
    simplification_dict = {}
    for word, following_words in word_neighbors.items():
        if len(following_words) == 1:
            following_word = following_words[0]
            if len(word_neighbors[following_word]) != 1:
                simplification_dict[f"{word} {following_word}"] = following_word
    dict_to_json(simplification_dict,"simplification_dict",folderName="saved_jsons/")
    return simplification_dict

def clean_aliases(d,pos=False):
    cleaned_dict = {}
    for award in d:
        for alias in d[award].aliases:
            cleaned_dict[alias] = clean_award_name(alias,pos=pos)
    dict_to_json(cleaned_dict,"clean_aliases",folderName="saved_jsons/")

def clean_award_name(awardName:str,pos=False)-> str:
    awardName = awardName.replace("for ","")
    awardName = awardName.replace(" in a","")
    awardName = awardName.replace(",","")
    awardName = awardName.replace("-","")
    awardName = awardName.replace(" in "," ")
    awardName = re.sub(' +',' ',awardName).strip()
    if pos:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(awardName)
        lastidx = 0
        for idx,token in enumerate(doc):
            if token.pos_ not in ['ADP','AUX','CCONJ','DET','INTJ','NUM','PRON','SCONJ']:
                lastidx = idx
        cleaned = ''.join([token.text  + " " for idx, token in enumerate(doc) if idx <= lastidx]).strip()
    return cleaned if pos else awardName

def print_keys(d):
    with open("test_files/keys.txt","w") as f:
        for k in d:
            f.write(f"\n{k}")

def get_award_categories_from_json(tweets):
    startTime = datetime.now()
    dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
    print("Find Award Names process started at =", dt_string)

    awards = find_awards(tweets)

    endFindAwardsTime = datetime.now()
    dt_string = endFindAwardsTime.strftime("%d/%m/%Y %H:%M:%S")
    print("Find Award Names process ended at =", dt_string)
    print("    duration:",str(endFindAwardsTime-startTime))

    startMergeAwardsTime = datetime.now()
    dt_string = startMergeAwardsTime.strftime("%d/%m/%Y %H:%M:%S")
    print("Merge Award Names process started at =", dt_string)

    clean_aliases(awards,pos=True)
    awards = merge_identical(awards)
    awards = merge_substrings(awards)
    awards = sort_dict_alpha(awards)
    clean_aliases(awards)
    word_neighbors = get_word_neighbors(awards)
    simpl_dict = get_simplification_dict(word_neighbors)
    awards = merge_simplify(awards,simpl_dict)
    awards = add_short_versions(awards)
    awards = sort_dict_alpha(awards)
    dict_to_json(awards,"award_aliases",award=True,folderName="")
    print_keys(awards)

    endTime = datetime.now()
    dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
    print("Merge Award Names process ended at =",dt_string)
    print("    duration:",str(endTime-startMergeAwardsTime))
    return awards

