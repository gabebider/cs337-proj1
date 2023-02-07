from Award import Award
import csv
from AwardCategory import AwardCategory
from aliases import get_aliases
import json
import spacy
import itertools
import re

# for testing purposes
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

# finds the winner given a list of awards
def findWinner(awards, tweets):
    for index in range(len(awards)):
        aliases = awards[index].award_category.aliases
        if re.search(r"\b(actor|actress|director|score)\b", aliases[0]):
            #timedTweets = Tweets_By_Time(tweets, aliases, 0.1)
            name_array = find_full_names(find_and_count_names(tweets, aliases))
            index2 = -1
            count = 0
            curr = -1
            for names in name_array:
                curr = curr + 1
                if names[1] > count:
                    index2 = curr
                    count = names[1]
            if index2 == -1:
                index2 = 0
                name_array.append(["no winner found", 0])
            awards[index].winner = name_array[index2][0]
        else:
            awards[index].winner = "movie placeholder"
    for a in awards:
        print(a.__str__())
    return awards

def find_and_count_names(data, aliases):
    # loads name processor
    langProcesor = spacy.load("en_core_web_sm")
    regex = r'\b(wins|win|winner|winning|won)\b.*\b({})\b|\b({})\b.*\b(wins|win|winner|winning|won)\b'.format('|'.join(aliases),'|'.join(aliases))
    #regex = r"\b(" + "|".join(aliases) + r")\b"
    nameCountArray = []
    tweetArray = []
    # Iterates through tweets
    for tweet in data:
        text = tweet['text']
        # Checks if tweet is relation to a host or hostess
        if  not text in tweetArray and re.search(regex, text.lower()):
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

findWinner(getAwards(), json.load(open('gg2013.json')))