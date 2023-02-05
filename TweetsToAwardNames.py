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
        text = standardize(tweet['text'].lower())
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
            text = standardize(tweet['text'].lower())
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
        set_to_name[cleanedAwardNameWords] = cleanedAwardName
        if cleanedAwardNameWords not in new_d:
            new_d[cleanedAwardNameWords] = AwardCategory(cleanedAwardName)
        else:
            print(f"merging {awardName} into {cleanedAwardName}")
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

        if len(substringOf) > 0:
            word = substringOf[substringOfValues.index(max(substringOfValues))]
            print(f"merging {awardName} into {word}")
            if len(substringOf) == 1:
                new_d[word].count += awardCategory.count
            new_d[word].aliases |= awardCategory.aliases
            merged = True
        if not merged:
            new_d[awardName] = awardCategory

    return new_d

def clean_aliases(d):
    cleaned_dict = {}
    for award in d:
        for alias in d[award].aliases:
            cleaned_dict[alias] = clean_award_name(alias)
    dict_to_json(cleaned_dict,"clean_aliases",folderName="saved_jsons")

def clean_award_name(awardName:str)-> str:
    awardName = awardName.replace("for ","")
    awardName = awardName.replace(" in a","")
    awardName = awardName.replace(",","")
    awardName = awardName.replace("-","")
    # awardName = re.sub(r'(for )|( in a)|(,)|(-)','',awardName)
    if "picture" in awardName and "motion picture" not in awardName:
        awardName = awardName.replace("picture","motion picture")
    if " series" in awardName and "tv series" not in awardName:
        awardName = awardName.replace(" series"," tv series")

    awardName = re.sub(' +',' ',awardName).strip()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(awardName)
    lastidx = 0
    for idx,token in enumerate(doc):
        if token.pos_ not in ['ADP','AUX','CCONJ','DET','INTJ','NUM','PRON','SCONJ']:
            lastidx = idx
    cleaned = ''.join([token.text  + " " for idx, token in enumerate(doc) if idx <= lastidx]).strip()
    return cleaned
    
def noun_identification(d):
    with open("test_files/noun_identification_test.txt",'w') as f:
        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe("merge_noun_chunks")
        for key in d:
            doc = nlp(key[5:])
            f.write(f"\n{key:} ")
            for token in doc:
                f.write(f"\n    {token.text}: {token.pos_}")

# def test_noun_chunks(d):
#     with open("test_files/noun_chunk_test.txt","w") as f:
#         nlp = spacy.load("en_core_web_sm")
#         for key in d:
#             doc = nlp(key[5:])
#             f.write(f"\n{key:} ")
#             for chunk in doc.noun_chunks:
#                 f.write(f"\n    {chunk.text},{chunk.root.text},{chunk.root.dep_},{chunk.root.head.text}")

# def combine_based_on_similarity(d):
#     nlp = spacy.load("en_core_web_sm")
#     similarity_dict = {}
#     for award1 in d:
#         print(award1)
#         award1_dict = {}
#         similarity_dict[award1] = award1_dict
#         for award2 in d:
#             print(award2)
#             similarities = []
#             for alias1 in d[award1].aliases:
#                 for alias2 in d[award2].aliases:
#                     doc1 = nlp(alias1[5:])
#                     doc2 = nlp(alias2[5:])
#                     similarities.append(doc1.similarity(doc2))
#             print(sum(similarities)/len(similarities))
#             award1_dict[award2] = sum(similarities)/len(similarities)
#     dict_to_json(similarity_dict,"similarity")
    

def print_keys(d):
    with open("test_files/keys.txt","w") as f:
        for k in d:
            f.write(f"\n{k}")

def test_or(d):
    alias_set = set()
    for k in d:
        alias_set |= d[k].aliases
    
    sorted_aliases = sorted(list(alias_set), key= lambda x: len(x.split()))

    with open("test_files/test_or.txt","w") as f:
        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe("merge_noun_chunks")
        for alias in sorted_aliases:
            doc = nlp(alias[5:])
            tokenlist = [token.text for token in doc]
            if "or" not in tokenlist:
                continue
            orInd = tokenlist.index("or")
            orWords = []
            if orInd < len(tokenlist)-1:
                orWords.append(tokenlist[orInd+1])
            if orInd > 0:
                orWords.append(tokenlist[orInd-1])
            if orInd > 3:
                if tokenlist[orInd-2] == ",":
                    orWords.append(tokenlist[orInd-3])
            f.write(f"\nOR: {alias} \n")
            for word in orWords:
                f.write(f"    {word}")

def get_award_categories():
    startTime = datetime.now()
    dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
    print("Find Award Names process started at =", dt_string)

    awards = find_awards(json.load(open('gg2013.json')))
    clean_aliases(awards)
    awards = merge_identical(awards)
    awards = merge_substrings(awards)
    awards = sort_dict_alpha(awards)

    dict_to_json(awards,"award_names_test",award=True)
    print_keys(awards)

    endTime = datetime.now()
    dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
    print("Find Award Names process ended at =", dt_string)
    print("Duration =",str(endTime-startTime))

get_award_categories()
