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
from utils import standardize, filter_and_sort_dict, dict_to_json, combine_permutations

def find_awards(tweets):
    uniqueAwards = defaultdict(int)

    seenTweets = set()
    for tweet in tweets:
        text = standardize(tweet['text'].lower())
        bestSearch = re.search(r"\s*(?P<award_name>[Bb]est .*) goes to",text)
        if bestSearch is not None and text not in seenTweets:
            seenTweets.add(text)
            uniqueAwards[bestSearch['award_name']] += 1

    uniqueAwards = filter_and_sort_dict(uniqueAwards,3)
    uniqueAwards = {k: 0 for k in uniqueAwards.keys()}

    for award in uniqueAwards:
        seenTweets = set()
        awardRegex = r"(\s*" + re.escape(award) + r".*)"
        for tweet in tweets:
            text = standardize(tweet['text'].lower())
            awardSearch = re.search(awardRegex,text)
            if awardSearch is not None and text not in seenTweets:
                seenTweets.add(text)
                uniqueAwards[award] += 1
        # print(award, uniqueAwards[award])
    uniqueAwards = {k: v for k, v in uniqueAwards.items() if 'speech' not in k}
    return filter_and_sort_dict(uniqueAwards,minCount=3,alpha=True)

# converts a dict of award names & counts to a dict of award names & AwardCategory objects
def convert_to_category(d):
   return {name: AwardCategory(name,count) for name, count in d.items()}


# def filter_award_name(awardName:str):
#     awardName = re.sub('for','',awardName)
#     awardName = re.sub(' +',' ',awardName).strip()
#     return awardName

def noun_identification(d):
    with open("noun_identification_test.txt",'w') as f:
        nlp = spacy.load("en_core_web_sm")
        for key, val in d.items():
            doc = nlp(key)
            f.write(f"\n{key:} ")
            for token in doc:
                f.write(f"\n    {token.text}: {token.pos_}")


def test():
    startTime = datetime.now()
    dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
    print("Find Award Names process started at =", dt_string)
    awards = find_awards(json.load(open('gg2013.json')))
    endTime = datetime.now()
    dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
    dict_to_json(awards,"award_names_test")
    noun_identification(awards)

    print("Find Award Names process ended at =", dt_string)
    print("Duration =",str(endTime-startTime))
    # perm_awards = combine_permutations(awards)
    # dict_to_json(perm_awards,"award_names_test_comb")

test()
