# Finds the best and worst red carpet outfits
import re
import csv
import itertools
from datetime import datetime
import spacy
import numpy as np
import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def find_and_count_names(data):
    # loads name processor
    langProcesor = spacy.load("en_core_web_md")
    nameCountArray = []
    tweetArray = []
    # Iterates through tweets
    for tweet in data:
        text = tweet['text']
        # Checks if tweet is relation to a host or hostess
        if re.search(r"\s*(red carpet|dress|outfit|fashion|suit|tuxedo|gown|taffetta|bow).*", text.lower()) and not text in tweetArray:
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


def most_discussed(actorCount):
    totalCount = 0
    # find total
    for entries in actorCount:
        totalCount = totalCount + entries[1]
    # display each percentage
    percentageArray = []
    actorPercentArray = []
    most_discussed = []
    for entries in actorCount:
        percentage = entries[1] / totalCount
        percentage = round(percentage, 3)
        #print(entries[0] + "'s Percentage: " + str(percentage))
        percentageArray.append(percentage)
        actorPercentArray.append([entries[0], percentage])
    # find three most mentioned actors by percentage
    for i in range(3):
        percent = 0
        name = ""
        for index in range(len(actorPercentArray)):
            if actorPercentArray[index][1] > percent:
                removeIndex = index
                percent = actorPercentArray[index][1]
                name = actorPercentArray[index][0]
        most_discussed.append(name)
        actorPercentArray.pop(removeIndex)
    return most_discussed

def best_and_worst_dressed(actorCount, tweets):
    dressedArray = []
    sentiment_analyzer = SentimentIntensityAnalyzer()
    # find sentiment of outfits 
    for actor in actorCount:
        name1 = actor[0].lower()
        name2 = actor[0].lower().replace(" ", "")
        pattern = f"{name1}|{name2}"
        sentimentCount = 0
        for tweet in tweets:
            if re.search(pattern, tweet.lower()):
                sentiment = sentiment_analyzer.polarity_scores(tweet)
                sentimentCount = sentimentCount + sentiment["compound"]
        dressedArray.append([actor[0], sentimentCount])
    bestDress = 0
    bestName = ""
    worstName = ""
    worstDress = 0
    # find the highest and lowest sentiments regarding people's outfits
    for outfits in dressedArray:
        if outfits[1] > bestDress:
            bestDress = outfits[1]
            bestName = outfits[0]
        elif outfits[1] < worstDress:
            worstDress = outfits[1]
            worstName = outfits[0]
    return [bestName, worstName]

def most_controversial(actorCount, tweets):
    dressedArray = []
    sentiment_analyzer = SentimentIntensityAnalyzer()
    # find sentiment of outfits 
    for actor in actorCount:
        sentimentArray = []
        name1 = actor[0].lower()
        name2 = actor[0].lower().replace(" ", "")
        pattern = f"{name1}|{name2}"
        for tweet in tweets:
            if re.search(pattern, tweet.lower()):
                sentiment = sentiment_analyzer.polarity_scores(tweet)
                sentimentArray.append(sentiment["compound"])
        # find variance of sentiments on this specific person
        variance = np.var(sentimentArray)
        dressedArray.append([actor[0], variance])
    dress = 0
    name = ""
    # find the person with the most variance in people's opinions
    for outfits in dressedArray:
        if outfits[1] > dress:
            dress = outfits[1]
            name = outfits[0]
    return name

def find_redcarpet(tweets):
    nltk.download("vader_lexicon")
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # print("Find Red Carpet Outfits process started at =", dt_string)
    nameCountAndTweets = find_and_count_names(tweets)
    fullNameCountArray = find_full_names(nameCountAndTweets[0])
    threeMostDiscussed = most_discussed(fullNameCountArray)
    bestWorstDressed = best_and_worst_dressed(fullNameCountArray, nameCountAndTweets[1])
    mostControversial = most_controversial(fullNameCountArray, nameCountAndTweets[1])
    # Put results in dictionary
    redCarpetResults = dict()
    redCarpetResults["Three Most Discussed"] = threeMostDiscussed
    redCarpetResults["Best Dressed"] = bestWorstDressed[0]
    redCarpetResults["Worst Dressed"] = bestWorstDressed[1]
    redCarpetResults["Most Controversial"] = mostControversial
    # Print results
    print("The three most discussed about people on the red carpet were: " + threeMostDiscussed[0] + ", " + threeMostDiscussed[1] + ", and " + threeMostDiscussed[2])
    print("The best dressed was: " + bestWorstDressed[0])
    print("The worst dressed was: " + bestWorstDressed[1])
    print("The most controversial person on the red carpet was: " + mostControversial)
    # now = datetime.now()
    # dt_string2 = now.strftime("%d/%m/%Y %H:%M:%S")
    # print("Find Red Carpet Outfits process ended at =", dt_string2)
    return redCarpetResults

#find_redcarpet(json.load(open('gg2013.json')))