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
from utils import standardize, wrap_regex
import json
from TweetsByTime import Tweets_By_Time

def build_iterative_regex(aliases):
    regexes = []
    for alias in aliases:
        regexes.append(wrap_regex(alias))
        regexes.append(r"|")
    regexes.pop()
    return ''.join(regexes)
        

def find_and_count_names_for_award(data,award_name):
    # loads name processor
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("merge_entities")
    nameCountArray = []
    tweetArray = []
    aliases = award_name.award_category.aliases
    data = Tweets_By_Time(data, aliases, 0.01)
    # Iterates through tweets
    for tweet in data:
        text = tweet['text']
        # Checks if tweet is relation to a presenter and a specific award
        ## re.search(r"\s*[Nn]omin.*", text) and
        if not text in tweetArray:
            tweetArray.append(text)
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
    # scraper.findActors()
    # load actors csv (scraped from imdb)
    fullNameArray = []
    singleNameArray = []
    finalNamesArray = []
    # create array of full names and single names
    for names in nameCountArray:
        if re.search(r".* .*", names[0]):
            fullNameArray.append([names[0], names[1]])
        else:
            singleNameArray.append([names[0], names[1]])
    with open('actors.csv', 'r', encoding='utf-8') as actorCSV:
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
    award_regex = r'(present|presents|presenter|presenting)'
    for actor in actorArray:
        name1 = actor[0].lower()
        name2 = actor[0].lower().replace(" ", "")
        pattern = f"{name1}|{name2}"
        for tweet in tweets:
            if re.search(pattern, tweet.lower()):
                if re.search(award_regex, tweet.lower()):
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
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # print("Find presenter process started at =", dt_string)
    nameCountAndTweetArray = find_and_count_names_for_award(tweets,award_name)
    fullNameCountArray = find_full_names(nameCountAndTweetArray[0])
    presenters = find_potential_presenters(fullNameCountArray, nameCountAndTweetArray[1])
    #presenters = find_name_std(potential_presenters)
    # if len(presenters) == 1:
    #     print("The presenter of the award show is: " + presenters[0])
    # else:
    #     print("The presenters of the award show are:")
    #     for presenter in presenters:
    #         print(presenter)
    # now = datetime.now()
    # dt_string2 = now.strftime("%d/%m/%Y %H:%M:%S")
    # print("Find presenter process ended at =", dt_string2)

    print(award_name.award_category, ":", presenters)
    # presenterStringArr = [f"{presenters[i]}" for i in range(len(presenters)-1)]
    # presenterStringArr.append(f"and {presenters[-1]}")
    # presenterString = ''.join(presenterStringArr)
    # print("The presenters of the",award_name,"are",presenterString)
    return presenters

# for testing purposes
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

# awards = getAwards()
# for award in awards:
#     pres = find_presenters(json.load(open('gg2013.json')), award)