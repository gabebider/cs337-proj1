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
    new_d = dict()
    d = dict(sorted(d.items(), key= lambda x: -len(x[0].split())))

    for awardName, awardCategory in d.items():
        cleanedAwardName = clean_award_name(awardName)
        if cleanedAwardName not in new_d:
            new_d[cleanedAwardName] = AwardCategory(cleanedAwardName)
        else:
            print(f"merging {awardName} into {cleanedAwardName}")
        new_d[cleanedAwardName].count += awardCategory.count
        new_d[cleanedAwardName].aliases |= awardCategory.aliases
    
    return new_d



def merge_substrings(d):
    new_d = dict()
    d = dict(sorted(d.items(), key= lambda x: -len(x[0].split())))

    for awardName, awardCategory in d.items():
        merged = False
        substringOf = []
        for mergedName in new_d:
            if awardName in mergedName:
                substringOf.append(mergedName)
        if len(substringOf) == 1:
            print(f"merging {awardName} into {substringOf[0]}")
            new_d[substringOf[0]].count += awardCategory.count
            new_d[substringOf[0]].aliases |= awardCategory.aliases
            merged = True
        if not merged:
            new_d[awardName] = awardCategory

    return new_d

def clean_award_name(awardName:str)-> str:
    awardName = re.sub(r'(for)|(in a)|(,)|(-)','',awardName)
    awardName = re.sub(' +',' ',awardName).strip()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(awardName)
    lastidx = 0
    for idx,token in enumerate(doc):
        if token.pos_ not in ['ADP','AUX','CCONJ','DET','INTJ','NUM','PRON','SCONJ']:
            lastidx = idx
    cleaned = ''.join([token.text  + " " for idx, token in enumerate(doc) if idx <= lastidx]).strip()
    if awardName != cleaned:
        print("")
        print(awardName)
        print(cleaned)
    return cleaned
    
def noun_identification(d):
    with open("test_files/noun_identification_test.txt",'w') as f:
        nlp = spacy.load("en_core_web_sm")
        for key in d:
            doc = nlp(key)
            f.write(f"\n{key:} ")
            for token in doc:
                f.write(f"\n    {token.text}: {token.pos_}")

def test_noun_chunks(d):
    with open("test_files/noun_chunk_test.txt","w") as f:
        nlp = spacy.load("en_core_web_sm")
        for key in d:
            doc = nlp(key[5:])
            f.write(f"\n{key:} ")
            for chunk in doc.noun_chunks:
                f.write(f"\n    {chunk.text},{chunk.root.text},{chunk.root.dep_},{chunk.root.head.text}")

def test():
    startTime = datetime.now()
    dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
    print("Find Award Names process started at =", dt_string)
    awards = find_awards(json.load(open('gg2013.json')))
    awards = merge_identical(awards)
    awards = merge_substrings(awards)
    # award_counts = {k:v.count for k,v in awards.items()}
    endTime = datetime.now()
    dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
    awards = sort_dict_alpha(awards)
    dict_to_json(awards,"award_names_test",award=True)
    # noun_identification(awards)
    # test_noun_chunks(awards)
    print("Find Award Names process ended at =", dt_string)
    print("Duration =",str(endTime-startTime))
    # perm_awards = combine_permutations(awards)
    # dict_to_json(perm_awards,"award_names_test_comb")

test()
