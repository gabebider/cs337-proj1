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