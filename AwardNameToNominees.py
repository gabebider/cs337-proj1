import json
import re
import csv
import itertools
from Award import Award
from AwardCategory import AwardCategory
from datetime import datetime
from collections import defaultdict
import spacy
import numpy as np
from aliases import award_aliases, get_aliases
from utils import standardize, build_iterative_regex

def AwardNameToNominees(tweets, awards, actors, movies):
    '''
    Finds the nominees for each award category

    Parameters
    ----------
    tweets : list[dict] (not sure if this is the right type, but the json file opened yknow)
    award_names : list[Award]
    actors : list[str]
    movies : list[str]

    Returns
    -------
    awards : list[Award]
    '''
    if not isinstance(awards, list):
        raise TypeError("award_names must be a list")
    if not all(isinstance(award, Award) for award in awards):
        raise TypeError("award_names must be a list of Award objects")

    def ultra_standardize(text):
        text = standardize(text)
        text = text.replace(".", "")
        text = text.replace(",", "")
        text = text.replace("!", "")
        text = text.replace("?", "")
        text = text.replace("@", "")
        text = text.replace("\"", "")
        text = text.replace("-", " ")
        text = text.lower()
        text = text.replace(" has ", "")
        return text
    
    # init dictionary to store votes for potential nominees
    nominee_votes = {}
    for award in awards:
        nominee_votes[award.award_category.award_name] = []
    
    # remove all duplicate tweets
    unique_tweets = []
    unique_text = set()
    for tweet in tweets:
        text = standardize(tweet['text'].lower())
        if text not in unique_text:
            unique_text.add(text)
            unique_tweets.append(tweet)
    # now we have a set of unique tweets to work with
    tweets = unique_tweets

    tracker = 0
     # loop through all tweets
    for tweet in tweets:
        if tracker % 5000 == 0:
            print(f"Looking at tweet {tracker} of {len(tweets)}")
        tracker += 1
        
        # just the text please
        tweet = ultra_standardize(tweet['text'])
        # loop through all awards
        for award in awards:
            # check all aliases for award names
            for alias in award.award_category.aliases:
                alias = ultra_standardize(alias)
                # check for the "X" won "Y" pattern
                # check_for_won_pattern(alias, tweet, award)
                # check_for_goes_to_pattern(alias, tweet, award)
                # check_for_wins_pattern(alias, tweet, award)
                


      

    # helper function to check for "X" wins "Y" pattern
    def check_for_wins_pattern(award_alias, tweet, award):
        if not isinstance(award_alias, str):
            raise TypeError("award_alias must be a string")
        if not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        if not isinstance(award, Award):
            raise TypeError("award must be an Award object")

        # this covers the "X" wins "Y" case
        # where "X" is the winner and "Y" is the award
        if award_alias in tweet and re.search(r" [Nn]ominated for ", tweet):
            try:
                nominated_index = tweet.lower().split().index("nominated")
            except:
                return
            for i in range(nominated_index - 1, -1, -1):
                nominee = ""
                for j in range(i, nominated_index):
                    nominee += tweet.split()[j] + " "
                nominee = nominee.strip()
                nominee_votes[award.award_category.award_name].append(nominee)
    




# def AwardNamesToNominees(tweets, awards, actors, movies):
#     '''
#     Finds the nominees for each award category

#     Parameters
#     ----------
#     tweets : list[dict] (not sure if this is the right type, but the json file opened yknow)
#     award_names : list[Award]
#     actors : list[str]
#     movies : list[str]

#     Returns
#     -------
#     awards : list[Award]
#     '''
#     # init dictionary to store votes for potential nominees
#     nominee_votes = {}
#     for award in awards:
#         nominee_votes[award.award_category.award_name] = defaultdict(int)

#     count = 0
#     for tweet in tweets:
#         if count % 100 == 0:
#             print(f"Checking tweet {count} of {len(tweets)}")
#         count +=1 
#         tweet = standardize(tweet['text']).lower()
#         for award in awards:
#             aliases = award.award_category.aliases
#             award_regex = build_iterative_regex(aliases)
#             for award_alias in award.award_category.aliases:
#                 if award_alias in tweet:
#                 # we found a tweet that mentions the given award
#                     if award.award_category.isPerson:
#                         # find an actor
#                         for actor in actors:
#                             try:
#                                 actor = standardize(actor).lower()
#                                 if re.search(rf"\b{actor}\b", tweet):
#                                     nominee_votes[award.award_category.award_name][actor] += 1
#                                     # break
#                             except:
#                                 continue
#                     else:
#                         # find a movie
#                         for movie in movies:
#                             # check if the movie is in the tweet with regex boundaries
#                             try:
#                                 movie = standardize(movie).lower()
#                                 if re.search(rf"\b{movie}\b", tweet):
#                                     nominee_votes[award.award_category.award_name][movie] += 1
#                                     # break
#                             except:
#                                 continue
                        
#     print("we done")
#     with open('test_files/nominees_pre_sort.json', 'w') as file:
#         json.dump(nominee_votes, file)

#     result = {k: dict(sorted(v.items(), key=lambda x: x[1], reverse=True)[:5]) for k, v in nominee_votes.items()}
#     print(result)
#     with open('test_files/nominees.json', 'w') as file:
#         json.dump(result, file)


# with open('actors.csv', 'r') as file:
#     reader = csv.reader(file)
#     actors = list(reader)
#     actors = actors.pop()

# with open('movies.csv', 'r') as file:
#     reader = csv.reader(file)
#     movies = list(reader)
#     movies = movies.pop()

# def getAwards():
#     awards = []
#     addedAwards = []
#     aliases = get_aliases()

#     # create list of awards
#     for cat in aliases:
#         if cat not in addedAwards:
#             addedAwards.append(cat)
#             awardStruct = Award(AwardCategory(cat))
#             awardStruct.award_category.aliases = aliases[cat]
#             awards.append(awardStruct)
#     return awards

# AwardNamesToNominees(json.load(open("gg2013.json")), getAwards(), actors, movies)