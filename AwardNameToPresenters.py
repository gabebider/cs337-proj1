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

def AwardNameToPresenters(award: Award, tweets, black_list):
    '''
    Finds the presenters for a given award

    Parameters:
        award: Award object
        tweets: list of tweets
        black_list: list of names to ignore (should be the winner and nominees of the award)
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


def tweets_for_time_interval(tweets, award_name_aliases: list, min_before: float, min_after: float):
    '''
        Finds the tweets in a given time interval
    '''
    return TweetsNearMedian(tweets, award_name_aliases, min_before=min_before, min_After=min_after)

def filter_tweets_for_good_words(tweets):
    '''
        Filters tweets to only include the tweets that mention the good words we found
    '''
    good_words = ["dress", "teleprompter", "looks", "love", "like", "funny", "next", "presenting", "gorgeous", "stunning", "beautiful", "hilarious", "dressed", "looking"]
    bad_words = ["acceptance"]
    good_words_regex = build_iterative_regex(good_words)
    bad_words_regex = build_iterative_regex(bad_words)
    return [tweet for tweet in tweets if re.search(good_words_regex, tweet['text']) and not re.search(bad_words_regex, tweet['text'])]

def filter_tweets_for_presenters(tweets):
    '''
        Use NER to find names in the tweets
    '''
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
    '''
        Returns the names of the best presenters
        If there is only one presenter, return that presenter
        If there are two presenters, return the two presenters if the second presenter is mentioned at least 60% as much as the first presenter

    '''
    if len(presenters) == 0:
        return []
    elif len(presenters) == 1:
        return [list(presenters.keys())[0]]
    elif len(presenters) >= 2:
        new_presenters = []
        new_presenters.append(list(presenters.keys())[0])
        if presenters[list(presenters.keys())[1]] * 0.6 < presenters[list(presenters.keys())[0]]:
            new_presenters.append(list(presenters.keys())[1])
        return new_presenters

def clean_results(results, bad_names):
    '''
        Removes the names of the winners and nominees from the results
    '''
    keys = list(results.keys())
    actors = get_csv_set("people.csv")
    new_results = {}
    for name in keys:
        if not name in bad_names and name in actors:
            new_results[name] = results[name]

    results = new_results
    return results
<<<<<<< Updated upstream
    
=======

def AwardNameToPresenters():

    award_aliases = json.load(open('award_aliases.json'))
    list_of__all_aliases = []
    alias_keys = list(award_aliases.keys())
    tweets = preprocess(json.load(open(f'gg2013.json')))
    results = {}
    for alias_key in alias_keys:
        results[alias_key] = presenters_for_award_alias(award_aliases[alias_key][1])
    #Sort all of the inner dicts of results by the number of times they were mentioned
    for key in results:
        results[key] = dict(sorted(results[key].items(), key=lambda item: item[1], reverse=True))
            

    # Step 1: Get the time interval for the start of the award
    # Step 2: Find the tweets in that time interval
    # Step 3: Filter those tweets to only include the tweets that mention the good words we found
    # Step 4: Use NER to find the names of the presenters
    # Step 5: Return the names of the presenters

    winner_and_nominees = set()
    data = json.load(open('autograder/gg2013answers.json'))
    keys = list(data['award_data'].keys())
    data = data["award_data"]

    for key in keys:
        for nominee in data[key]["nominees"]:
            winner_and_nominees.add(nominee)
        winner_and_nominees.add(data[key]["winner"])

    results = clean_results(results, winner_and_nominees)

    newResult = {}
    for result in results:
        if len(result.keys()) == 1:
            newResult[list(results[result].keys())[0]] = results[result][list(results[result].keys())[0]]
            continue
        if len(result > 1):
            # If the first two presenters have more than 3 mentions, then we are done
            # Add them to the new result
            if results[result][list(results[result].keys())[1]] > 3:
                newResult[list(results[result].keys())[1]] = results[result][list(results[result].keys())[1]]
        
    return results

if __name__ == "__main__":
    results = AwardNameToPresenters()
    with open('results_new_new.json', 'w') as f:
        json.dump(results, f, indent=4) 
>>>>>>> Stashed changes
