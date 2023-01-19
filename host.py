# finds the host (or hosts) of the award show
from nltk.tag import StanfordNERTagger
import json
import re
import nltk
import csv
import itertools
from scipy.stats import norm
import math
#import scraper

def find_and_count_names():
    #loads json and name tagger
    data = json.load(open('gg2013.json'))
    nltk.download('punkt')
    tagger = StanfordNERTagger('classifiers/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz','classifiers/stanford-ner/stanford-ner.jar',encoding='utf-8')
    nameCountArray = []
    # Iterates through tweets
    for tweet in data:
        text = tweet['text']
        # Checks if tweet is relation to a host or hostess
        if re.match(r".* host | hostess .*", text):
            addNames = []
            tokenizedText = nltk.word_tokenize(text)
            classifiedText = tagger.tag(tokenizedText)
            # adds name to list
            for name in classifiedText:
                if name[1] == 'PERSON':
                    addNames.append(name[0])
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
    #scraper.findActors()
    # load actors csv (scraped from imdb)
    fullNameArray = []
    with open('actors.csv', 'r', encoding='utf-8') as actorCSV:
        reader = csv.reader(actorCSV)
        actorsArray = list(next(reader))
        # find all possible name combinations
        for i in range(len(nameCountArray)):
            for j in range(len(nameCountArray)):
                currentName = nameCountArray[i][0] + " " + nameCountArray[j][0]
                count = nameCountArray[i][1] + nameCountArray[j][1]
                # check if name combination is an actor
                for actor in actorsArray:
                    if currentName == actor:
                        fullNameArray.append([actor, count])
    # remove duplicate names
    fullNameArray = [x[0] for x in itertools.groupby(fullNameArray)]
    return fullNameArray

def find_name_percentage(actorCount):
    totalCount = 0
    highest_percent = ["", 0.0]
    # find total
    for entries in actorCount:
        totalCount = totalCount + entries[1]
    # display each percentage
    for entries in actorCount:
        percentage = entries[1] / totalCount
        percentage = round(percentage, 3)
        #print(entries[0] + "'s Percentage: " + str(percentage))
        if percentage > highest_percent[1]:
            highest_percent = [entries[0], percentage]
    # use z-score to determine if count is significantly different to highest percent (which should be host) to determine if more than one host
    stError = math.sqrt(highest_percent[1] * (1 - highest_percent[1]) / totalCount)
    host_array = []
    for entries in actorCount:
        percentage = entries[1] / totalCount
        zScore = (percentage - highest_percent[1]) / stError
        p_value = 2 * (1 - norm.cdf(abs(zScore)))
        #print(entries[0] + "'s P-Value: " +  str(p_value) + " and Z-Score: " + str(zScore))
        if p_value > 0.05:
            host_array.append(entries[0])
    return host_array

def find_host():
    nameCountArray = find_and_count_names()
    #nameCountArray = [['Tina', 277], ['Fey', 152], ['Amy', 285], ['Poehler', 150], ['Pohler', 4], ['VanityFair', 3], ['Ricky', 3], ['Gervais', 3], ['Oscar', 1], ['Hathaway', 1], ['Franko', 1], ['Al', 1], ['Roker', 1], ['poehler', 2], ['fey', 3], ['Kaley', 1], ['Cuoco', 1], ['AntDeRosa', 1], ['Fay', 1], ['KreeBeau', 1], ['Poehlr', 1], ['JayHandelman', 1], ['Elmo', 2], ['Matt', 1], ['Pinfield', 1], ['Toby', 1], ['Rudd', 47], ['Selma', 1], ['Hayek', 1], ['Paul', 46], ['Seth', 1], ['Poleher', 1], ['Kristin', 3], ['Wigg', 1], ['Clinton', 3], ['Maggie', 7], ['Smith', 3], ['Bill', 2], ['Rodham', 1], ['GoldenGlobes', 1], ['Rebel', 3], ['Wilson', 3], ['Fat', 3], ['Ellen', 2], ['Wiig', 124], ['Ferrell', 124], ['Smi', 4], ['Will', 123], ['Kristen', 126], ['Maya', 1], ['DeGeneres', 1], ['Wig', 2], ['Farrell', 1]]
    fullNameCountArray = find_full_names(nameCountArray)
    hosts = find_name_percentage(fullNameCountArray)
    if len(hosts) == 1:
        print("The host of the award show is: " + hosts[0])
    else:
        print("The hosts of the award show are:")
        for host in hosts:
            print(host)
    return hosts

find_host()