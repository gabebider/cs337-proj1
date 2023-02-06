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

def AwardNameToNominees(tweets, award):
    '''
    Finds the nominees for each award category

    Parameters
    ----------
    tweets : list[dict] (not sure if this is the right type, but the json file opened yknow)
    award : Award (the award we are trying to find the nominees for)

    Returns
    -------
    nominees : list[str] (the names of the nominees)
    '''
    if not isinstance(award, Award):
        raise TypeError("award must be a list")

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

    # helper function to check for "X" wins "Y" pattern
    def check_for_should_win_pattern(award_alias, tweet, award):
        if not isinstance(award_alias, str):
            raise TypeError("award_alias must be a string")
        if not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        if not isinstance(award, Award):
            raise TypeError("award must be an Award object")

        # this covers the "X" should win "Y" case
        # where "X" is the nominee and "Y" is the award
        if award_alias in tweet and re.search(r" should win ", tweet):
            try:
                nominated_index = tweet.lower().split().index("should")
            except:
                return
            for i in range(nominated_index - 1, -1, -1):
                nominee = ""
                for j in range(i, nominated_index):
                    nominee += tweet.split()[j] + " "
                nominee = nominee.strip()
                nominee_canidates.append(nominee)

    def check_for_pattern(award_alias, tweet, award, pattern, forward: bool):
        if not isinstance(forward, bool):
            raise TypeError("forward must be a boolean")
        if not isinstance(award_alias, str):
            raise TypeError("award_alias must be a string")
        if not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        if not isinstance(award, Award):
            raise TypeError("award must be an Award object")
        
        if award_alias in tweet and re.search( rf" {pattern} ", tweet):
            # TODO: add try except here 
            if len(pattern.split()) > 1 and forward:
                nominated_index = tweet.lower().split().index(pattern.split()[-1])
            elif len(pattern.split()) > 1 and not forward:
                nominated_index = tweet.lower().split().index(pattern.split()[0])
            else:
                nominated_index = tweet.lower().split().index(pattern)

            if forward:
                for i in range(nominated_index + 1, len(tweet.split())):
                    nominee = ""
                    for j in range(nominated_index + 1, i + 1):
                        nominee += tweet.split()[j] + " "
                    nominee = nominee.strip()
                    nominee_canidates.append(nominee)
            else:
                for i in range(nominated_index - 1, -1, -1):
                    nominee = ""
                    for j in range(i, nominated_index):
                        nominee += tweet.split()[j] + " "
                    nominee = nominee.strip()
                    nominee_canidates.append(nominee)
        
    
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

    nominee_canidates = []
    tracker = 0
     # loop through all tweets
    for tweet in tweets:
        if tracker % 5000 == 0:
            print(f"Looking at tweet {tracker} of {len(tweets)}")
        tracker += 1
        
        # just the text please
        tweet = ultra_standardize(tweet['text'])
        # check all aliases for award names
        for alias in award.award_category.aliases:
            alias = ultra_standardize(alias)
            check_for_pattern(alias, tweet, award, "should win", False)
            check_for_pattern(alias, tweet, award, "should have won", False)
            check_for_pattern(alias, tweet, award, "should have been", False)
            check_for_pattern(alias, tweet, award, "should have gotten", False)
            check_for_pattern(alias, tweet, award, "robbed", False)
            
            # check_for_goes_to_pattern(alias, tweet, award)
            # check_for_wins_pattern(alias, tweet, award)

    winner = max(nominee_canidates, key=lambda x: (nominee_canidates.count(x), len(x)))
    if len(nominee_canidates) == 0:
        winner = "No winner found"
        award.winner = winner
    else:
        award.winner = winner

    return winner
            


def getAwards():
    awards = []
    addedAwards = []
    aliases = get_aliases()

    # create list of awards
    for cat in aliases:
        if cat not in addedAwards:
            addedAwards.append(cat)
            awardStruct = Award(AwardCategory(cat))
            awardStruct.award_category.aliases = aliases[cat]
            awards.append(awardStruct)
    return awards

print(AwardNameToNominees(json.load(open('gg2013.json')), getAwards()[0]))




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