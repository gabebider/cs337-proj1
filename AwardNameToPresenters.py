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
from EliWhat import EliWhat
        

def find_and_count_names_for_award(data,award_name):
    # loads name processor
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("merge_entities")
    nameCountArray = []
    tweetArray = set()
    aliases = award_name.award_category.aliases
    #data = Tweets_By_Time(data, aliases, 0.4)
    data = EliWhat(data, aliases)
    # Iterates through tweets
    for tweet in data:
        text = tweet['text']
        # Checks if tweet is relation to a presenter and a specific award
        if not text in tweetArray:
            tweetArray.add(text)
            addNames = []
            classifiedText = nlp(text)
            # adds name to list
            for name in classifiedText.ents:
                if name.label_ == "PERSON":
                    addNames.append(name.text)
            # updates count if name exists or adds name if does not exist yet
            for name in addNames:
                exists = False
                for entries in nameCountArray:
                    if entries[0] == name:
                        exists = True
                        entries[1] = entries[1] + 1
                if exists == False:
                    nameCountArray.append([name, 1])
    return [nameCountArray, tweetArray]


def find_full_names(nameCountArray):

    fullNameArray = []
    singleNameArray = []
    finalNamesArray = []

    for names in nameCountArray:
        if re.search(r".* .*", names[0]):
            fullNameArray.append([names[0], names[1]])
        else:
            singleNameArray.append([names[0], names[1]])
    with open('people.csv', 'r', encoding='utf-8') as actorCSV:
        reader = csv.reader(actorCSV)
        actorsArray = list(next(reader))
        # find full names that are actors
        for actor in fullNameArray:
            if actor[0] in actorsArray:
                finalNamesArray.append([actor[0], actor[1]])
    for name in singleNameArray:
        for x in range(len(finalNamesArray)):
            if name[0] in finalNamesArray[x][0]:
                if finalNamesArray[x][1] > name[1]:
                    finalNamesArray[x][1] = finalNamesArray[x][1] + name[1]
    # remove duplicate names
    finalNamesArray = [x[0] for x in itertools.groupby(finalNamesArray)]
    return finalNamesArray

def find_potential_presenters(actorArray, tweets):
    potentialPresenters = []
    award_regex = r'( introduce| present)'
    tweets = list(tweets)
    for actor in actorArray:
        name1 = actor[0].lower()
        name2 = actor[0].lower().replace(" ", "")
        pattern = f"{name1}|{name2}"
        added = False
        for tweet in tweets:
            if re.search(pattern, tweet.lower()) and added == False:
                if re.search(award_regex, tweet.lower()):
                    added = True
                    potentialPresenters.append(actor[0])
    return potentialPresenters

# def find_name_std(actorCount):
#     totalCount = 0
#     # find total
#     for entries in actorCount:
#         totalCount = totalCount + entries[1]
#     # display each percentage
#     percentageArray = []
#     actorPercentArray = []
#     presenter_array = []
#     for entries in actorCount:
#         percentage = entries[1] / totalCount
#         percentage = round(percentage, 3)
#         print(entries[0] + "'s Percentage: " + str(percentage))
#         percentageArray.append(percentage)
#         actorPercentArray.append([entries[0], percentage])
#     # use standard deviation to determine if count is significantly different (outside 95% of data) to determine who the presenters are
#     mean = np.mean(percentageArray)
#     stanDev = np.std(percentageArray)
#     for entries in actorPercentArray:
#         print(entries[0] + "'s Standard Deviation: " + str((entries[1] - mean) / stanDev))
#         if abs(entries[1] - mean) > 2 * stanDev:
#             presenter_array.append(entries[0])
#     return presenter_array

def find_presenters(tweets,award_name):
    nameCountAndTweetArray = find_and_count_names_for_award(tweets,award_name)
    fullNameCountArray = find_full_names(nameCountAndTweetArray[0])
    presenters = find_potential_presenters(fullNameCountArray, nameCountAndTweetArray[1])

    # print(award_name.award_category, ":", presenters)

    return presenters

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

awards = getAwards()
for award in awards:
    pres = find_presenters(preprocess(json.load(open('gg2013.json'))), award)
    #exit()