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
from utils import standardize, build_iterative_regex, dict_to_json, sort_dict_decreasing_count
from TweetsByTime import Tweets_By_Time

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

    def check_for_pattern(tweet, award, pattern, forward: bool):
        if not isinstance(forward, bool):
            raise TypeError("forward must be a boolean")
        if not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        if not isinstance(award, Award):
            raise TypeError("award must be an Award object")
        
        if re.search( rf" {pattern} ", tweet):
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
                    nominee_canidates[nominee] += 1
            else:
                for i in range(nominated_index - 1, -1, -1):
                    nominee = ""
                    for j in range(i, nominated_index):
                        nominee += tweet.split()[j] + " "
                    nominee = nominee.strip()
                    nominee_canidates[nominee] += 1

    def check_for_people(tweet):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(ultra_standardize(tweet))
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                nominee_canidates[ent.text] += 1

    
    award_aliases = award.award_category.aliases
    relevant_tweets = Tweets_By_Time(tweets=tweets,award_name_aliases=award_aliases,range=0.3)
    # remove all duplicate tweets
    unique_tweets = []
    unique_text = set()
    for tweet in relevant_tweets:
        text = standardize(tweet['text'].lower())
        if text not in unique_text:
            unique_text.add(text)
            unique_tweets.append(tweet)
    # now we have a set of unique tweets to work with
    tweets = unique_tweets

    nominee_canidates = defaultdict(int)
    tracker = 0
     # loop through all tweets
    for tweet in tweets:
        if tracker % 5000 == 0:
            print(f"Looking at tweet {tracker} of {len(tweets)}")
        tracker += 1
        
        # just the text please
        tweet = ultra_standardize(tweet['text'])
        # check all aliases for award names
        check_for_pattern(tweet, award, "should win", False)
        check_for_pattern(tweet, award, "should have won", False)
        check_for_pattern(tweet, award, "shouldn't have won", False)
        # check_for_pattern(tweet, award, "should have won", False)
        check_for_pattern(tweet, award, "should have been", False)
        check_for_pattern(tweet, award, "shouldn't have been", False)
        check_for_pattern(tweet, award, "should have gotten", False)

    # please don't judge me for this
    if award.award_category.isPerson:
        SUPERMEGATWEET = ''.join(tweet["text"] + " " for tweet in tweets[:3000])
        check_for_people(SUPERMEGATWEET)

        # check_for_pattern(tweet, award, "robbed", False)
        
        # check_for_goes_to_pattern(alias, tweet, award)
        # check_for_wins_pattern(alias, tweet, award)


    nominee_candidates = {k:v for k,v in nominee_candidates.items() if v>1}
    nominee_candidates = dict(sorted(nominee_candidates.items(), key=lambda x: -x[1]))
    
    actors = get_csv_set("actors.csv")
    movies = get_csv_set("movies.csv")

    if award.award_category.isPerson:
        nominee_candidates = {k:v for k,v in nominee_candidates.items() if k in actors}
    else:
        nominee_candidates = {k:v for k,v in nominee_candidates.items() if k in movies}
    
    return [nom for i,nom in enumerate(nominee_candidates.keys()) if i < 5]

    # winner = max(nominee_canidates, key=lambda x: (nominee_canidates.count(x), len(x)))
    # if len(nominee_canidates) == 0:
    #     winner = "No winner found"
    #     award.winner = winner
    # else:
    #     award.winner = winner

    # return winner


def get_csv_set(csv_file):
    csvSet = set()
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for name in row:
                csvSet.add(name.lower())
    return csvSet



def test():
    with open("test_files/award_names_test.json", "r") as file:
        awards = json.load(file)

    tweets = json.load(open(f'gg2013.json'))

    actors = get_csv_set("actors.csv")
    movies = get_csv_set("movies.csv")

    aaaa = dict()
    i = 0
    for key,award in awards.items():
        awc = AwardCategory(key)
        awc.aliases = award[1]
        awc.count = award[0]
        aw = Award(awc)
        i += 1

        nom_candidates = AwardNameToNominees(tweets, aw)
        nom_candidates = {k:v for k,v in nom_candidates.items() if v>1}
        nom_candidates = dict(sorted(nom_candidates.items(), key=lambda x: -x[1]))
        
        if awc.isPerson:
            nom_candidates = {k:v for k,v in nom_candidates.items() if k in actors}
        else:
            nom_candidates = {k:v for k,v in nom_candidates.items() if k in movies}

        aaaa[aw.award_category.award_name] = nom_candidates
    
        # if i == 5:
        #     break
    dict_to_json(aaaa,"aaaa",False,"test_files")

test()
    


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

# print(AwardNameToNominees(json.load(open('gg2013.json')), getAwards()[0]))




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