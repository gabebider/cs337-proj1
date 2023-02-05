import re
import csv
import itertools
from datetime import datetime
from collections import defaultdict
import spacy
import numpy as np
from aliases import award_aliases
from utils import standardize, wrap_regex

def build_iterative_regex(aliases):
    regexes = []
    for alias in aliases:
        regexes.append(wrap_regex(alias))
        regexes.append(r"|")
    regexes.pop()
    return ''.join(regexes)
        

def find_and_count_names_for_award(data,award_name):
    # loads name processor
    nlp = spacy.load("en_core_web_md")
    nlp.add_pipe("merge_entities")
    nameCountArray = []
    nameCountDict = defaultdict(int)
    properNounDict = defaultdict(int)
    tweetArray = []
    aliases = award_aliases[award_name.award_category]
    award_regex = build_iterative_regex(aliases)
    print("")
    print(award_name.award_category)
    # Iterates through tweets
    for tweet in data:
        text = standardize(tweet['text'].lower())
        # Checks if tweet is relation to a presenter and a specific award
        ## re.search(r"\s*[Nn]omin.*", text) and
        if re.search(award_regex, text) and not text in tweetArray:
            tweetArray.append(text)
            # print(text)
            addNames = []
            doc = nlp(text)

            for token in doc:
                if token.pos_ == "PROPN":
                    # print(token, token.pos_)
                    properNounDict[token.text] += 1

            for name in doc.ents:
                if name.label_ == "PERSON":
                    # print(name.text)
                    addNames.append(name.text)
            # updates count if name exists or adds name if does not exist yet
            for name in addNames:
                nameCountDict[name] += 1
                exists = False
                for entries in nameCountArray:
                    if entries[0] == name:
                        exists = True
                        entries[1] = entries[1] + 1
                if exists == False:
                    nameCountArray.append([name, 1])

    for pm, count in list(properNounDict.items()):
        if count <= 1:
            del properNounDict[pm]

    for name, count in list(nameCountDict.items()):
        if count <= 1:
            del nameCountDict[name]
    print(properNounDict)
    print(nameCountDict)
    return nameCountArray


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


def find_name_std(actorCount):
    totalCount = 0
    # find total
    for entries in actorCount:
        totalCount = totalCount + entries[1]
    # display each percentage
    percentageArray = []
    actorPercentArray = []
    presenter_array = []
    for entries in actorCount:
        percentage = entries[1] / totalCount
        percentage = round(percentage, 3)
        print(entries[0] + "'s Percentage: " + str(percentage))
        percentageArray.append(percentage)
        actorPercentArray.append([entries[0], percentage])
    # use standard deviation to determine if count is significantly different (outside 95% of data) to determine who the presenters are
    mean = np.mean(percentageArray)
    stanDev = np.std(percentageArray)
    for entries in actorPercentArray:
        print(entries[0] + "'s Standard Deviation: " + str((entries[1] - mean) / stanDev))
        if abs(entries[1] - mean) > 2 * stanDev:
            presenter_array.append(entries[0])
    return presenter_array


def find_presenters(tweets,award_name):
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # print("Find presenter process started at =", dt_string)
    nameCountArray = find_and_count_names_for_award(tweets,award_name)
    fullNameCountArray = find_full_names(nameCountArray)
    presenters = find_name_std(fullNameCountArray)
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