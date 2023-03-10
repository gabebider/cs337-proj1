# finds the host (or hosts) of the award show
import re
import csv
import itertools
import spacy
import numpy as np
from utils import get_csv_set
#import scraper


def find_and_count_names(data):
    # loads name processor
    langProcesor = spacy.load("en_core_web_md")
    nameCountArray = []
    tweetArray = []
    # Iterates through tweets
    for tweet in data:
        text = tweet['text']
        # Checks if tweet is relation to a host or hostess
        if re.search(r"\s*[Hh]ost.*", text) and not text in tweetArray:
            tweetArray.append(text)
            addNames = []
            classifiedText = langProcesor(text)
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


def find_name_std(actorCount):
    totalCount = 0
    # find total
    for entries in actorCount:
        totalCount = totalCount + entries[1]
    # display each percentage
    percentageArray = []
    actorPercentArray = []
    host_array = []
    for entries in actorCount:
        percentage = entries[1] / totalCount
        percentage = round(percentage, 3)
        # print(entries[0] + "'s Percentage: " + str(percentage))
        percentageArray.append(percentage)
        actorPercentArray.append([entries[0], percentage])
    # use standard deviation to determine if count is significantly different (outside 95% of data) to determine who the hosts are
    mean = np.mean(percentageArray)
    stanDev = np.std(percentageArray)
    for entries in actorPercentArray:
        #print(entries[0] + "'s Standard Deviation: " + str((entries[1] - mean) / stanDev))
        if abs(entries[1] - mean) > 2 * stanDev:
            host_array.append(entries[0])
    return host_array


def find_host(tweets):
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # print("Find Host process started at =", dt_string)
    nameCountArray = find_and_count_names(tweets)
    fullNameCountArray = find_full_names(nameCountArray)
    hosts = find_name_std(fullNameCountArray)
    # if len(hosts) == 1:
    #     print("The host of the award show is: " + hosts[0])
    # else:
    #     print("The hosts of the award show are:")
    #     for host in hosts:
    #         print(host)
    # now = datetime.now()
    # dt_string2 = now.strftime("%d/%m/%Y %H:%M:%S")
    # print("Find Host process ended at =", dt_string2)
    return [host.lower() for host in hosts]