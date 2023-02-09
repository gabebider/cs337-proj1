import re
import csv
import itertools
from datetime import datetime
from collections import defaultdict
import spacy
import numpy as np
from aliases import award_aliases
from aliases import get_aliases
from Award import Award
from AwardCategory import AwardCategory
from utils import standardize, wrap_regex, build_iterative_regex
import json
from TweetsByTime import Tweets_By_Time
from utils import preprocess, standardize, get_csv_set, dict_to_json
from TweetsNearMedian import TweetsNearMedian

# Step 1: Get the time interval for the start of the award
# Step 2: Find the tweets in that time interval
# Step 3: Filter those tweets to only include the tweets that mention the good words we found
# Step 4: Use NER to find the names of the presenters
# Step 5: Return the names of the presenters

# CALL MEEEEEE
def presenters_for_award(award: Award, tweets, black_list):
    '''
    Finds the presenters for a given award
    Parameters:
        award: Award object
        tweets: list of tweets
        black_list: list of names to ignore
    Returns:
        list of presenters
    '''
    aliases = award.award_category.aliases
    new_tweets = tweets_for_time_interval(tweets, aliases, min_before=2, min_after=1)
    new_tweets = filter_tweets_for_good_words(new_tweets)
    presenters = filter_tweets_for_presenters(new_tweets)
    presenters = clean_results(presenters, black_list)
    presenters = pick_best_presenters(presenters)
    return presenters


# Step 1: Get the time interval for the start of the award
# Step 2: Find the tweets in that time interval
def tweets_for_time_interval(tweets, award_name_aliases: list, min_before: float, min_after: float):
    return TweetsNearMedian(tweets, award_name_aliases, min_before=min_before, min_After=min_after)

# Step 3: Filter those tweets to only include the tweets that mention the good words we found
def filter_tweets_for_good_words(tweets):
    good_words = ["dress", "teleprompter", "looks", "love", "like", "funny", "next", "presenting", "gorgeous", "stunning", "beautiful", "hilarious", "dressed", "looking"]
    bad_words = ["acceptance"]
    good_words_regex = build_iterative_regex(good_words)
    bad_words_regex = build_iterative_regex(bad_words)
    return [tweet for tweet in tweets if re.search(good_words_regex, tweet['text']) and not re.search(bad_words_regex, tweet['text'])]

# Step 4: Use NER to find the names of the presenters
def filter_tweets_for_presenters(tweets):
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("merge_entities")
    presenters = {}
    for tweet in tweets:
        classified_text = nlp(tweet['text'])
        for name in classified_text.ents:
            if name.label_ == "PERSON":
                if name.text.lower() in presenters:
                    presenters[name.text.lower()] += 1
                else:
                    presenters[name.text.lower()] = 1
    # Sort the presenters by the number of times they were mentioned and make them a dict
    presenters = dict(sorted(presenters.items(), key=lambda item: item[1], reverse=True))
    return presenters

# Step 5: Return the names of the best presenters
def pick_best_presenters(presenters):
    # TODO - pick the best presenters
    if len(presenters) == 0:
        return []
    elif len(presenters) == 1:
        return [list(presenters.keys())[0]]
    elif len(presenters) >= 2:
        new_presenters = []
        new_presenters.append(list(presenters.keys())[0])
        if presenters[list(presenters.keys())[0]] * 0.6 < presenters[list(presenters.keys())[1]]:
            new_presenters.append(list(presenters.keys())[0])
        return new_presenters

def clean_results(results, bad_names):
    keys = list(results.keys())
    actors = get_csv_set("people.csv")
    new_results = {}
    for name in keys:
        if not name in bad_names and name in actors:
            new_results[name] = results[name]

    results = new_results
    return results

#for testing purposes
def getAwards():
    with open("award_aliases.json", "r") as file:
        awards = json.load(file)

    addedAwards = []
    awardsList = []
    # create list of awards
    for cat in awards:
        if cat not in addedAwards:
            addedAwards.append(cat)
            awardStruct = Award(AwardCategory(cat))
            currAlias = awards[cat][1]
            awardStruct.award_category.aliases = currAlias
            awardsList.append(awardStruct)
    # for a in awardsList:
    #     print(a.__str__() + " " + str(a.award_category.aliases))
    return awardsList