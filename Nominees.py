from Award import Award
import csv
from AwardCategory import AwardCategory
from aliases import get_aliases
from TweetsByTime import Tweets_By_Time
import json
import spacy
import itertools
import re

# gets the nominees from the csv file, for testing purposes
def getNominees():
    # Open the CSV file and read the data into a list
    with open("golden_globe_awards.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Filter the data to only include films from 2013
    filtered_data = [row for row in data if row[1] == "2013"]

    # Create a dictionary to store the award information
    awards = {}

    # Loop through the filtered data and add the award information to the dictionary
    for row in filtered_data:
        category = row[3].lower()
        nominee = row[4].lower().strip()
        film = row[5].lower().replace("\t", "").strip()
        win = row[6]

        # Check if the award already exists in the dictionary
        if category not in awards:
            # If it doesn't, create a new entry for the award
            awards[category] = {"winner": None, "nominees": []}

        # Add the nominee information to the dictionary
        awards[category]["nominees"].append(
            {"nominee": nominee, "film": film})

        # If the nominee won, update the winner property
        if win == "True":
            awards[category]["winner"] = {"nominee": nominee, "film": film}

    # print(awards)
    return awards

# returns list of awards, used for testing purposes
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

# finds the nominees given a list of awards
def findNominees(awards, tweets):
    for index in range(len(awards)):
        aliases = awards[index].award_category.aliases
        # check if the award is a movie or a person
        if re.search(r"\b(actor|actress|director|score)\b", aliases[0]):
            # print(awards[index].__str__())
            timedTweets = Tweets_By_Time(tweets, aliases, 0.30)
            # print(r"\b(" + "|".join(aliases) + r")\b")
            name_array = find_full_names(find_and_count_names(timedTweets, aliases))
            name_array = sorted(name_array, key=lambda x: x[1])
            print(awards[index].award_category.award_name)
            print(name_array)
            print("")
        else:
            print("movie names")
            print(awards[index].__str__())
            print("")

def find_and_count_names(data, aliases):
    # loads name processor
    langProcesor = spacy.load("en_core_web_sm")
    nameCountArray = []
    tweetArray = []
    # Iterates through tweets
    for tweet in data:
        text = tweet['text']
        # Checks if tweet is relation to a host or hostess
        if  not text in tweetArray and re.search(r"\b(" + "|".join(aliases) + "|nominee|nominees|nominated|nominate|nomination" + r")\b", text.lower()):
            # print(text)
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

findNominees(getAwards(), json.load(open('gg2013.json')))