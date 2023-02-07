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
            timedTweets = Tweets_By_Time(tweets, aliases, 0.6)
            name_array = find_full_names(find_and_count_names(timedTweets, aliases))
            name_array = dict(sorted(name_array.items(), key=lambda item: item[1], reverse=True))
            print(awards[index].award_category.award_name)
            print(name_array)
            print("")
        else:
            print("movie names")
            print(awards[index].award_category.award_name)
            print("")

def find_and_count_names(data, aliases):
    # loads name processor
    langProcesor = spacy.load("en_core_web_sm")
    nameCounts = {}
    tweetArray = []
    # Iterates through tweets
    for tweet in data:
        text = tweet['text']
        # Checks if tweet is relation to a host or hostess
        if  not text in tweetArray and re.search(r"\b(" + "|".join(aliases) + "stole|rob|should have won" + r")\b", text.lower()): # |nominee|nominees|nominated|nominate|nomination
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
                if name in nameCounts:
                    nameCounts[name] = nameCounts[name] + 1
                else:
                    nameCounts[name] = 1
    return nameCounts


def find_full_names(nameCounts):
    # scraper.findActors()
    # load actors csv (scraped from imdb)
    fullNames = {}
    singleNames = {}
    finalNames = {}
    # create array of full names and single names
    for name in nameCounts.keys():
        if " " in name:
            fullNames[name] = nameCounts[name]
        else:
            singleNames[name] = nameCounts[name]
    with open('people.csv', 'r', encoding='utf-8') as actorCSV:
        reader = csv.reader(actorCSV)
        actorsArray = list(next(reader))
        # find full names that are actors
        for actor in fullNames.keys():
            if actor in actorsArray:
                finalNames[actor] = fullNames[actor]

    for name in singleNames.keys():
        # find single names that are actors
        # for actor in actorsArray:
        #     if name in actor:
        #         if actor in finalNames:
        #             finalNames[actor] = finalNames[actor] + singleNames[name]
        #         else:
        #             finalNames[actor] = singleNames[name]
        if name in finalNames:
            finalNames[name] = finalNames[name] + singleNames[name]
        else:
            finalNames[name] = singleNames[name]
    # remove duplicate names
    # finalNamesArray = [x[0] for x in itertools.groupby(finalNamesArray)]
    return finalNames

if __name__ == "__main__":
    findNominees(getAwards(), json.load(open('gg2013.json')))