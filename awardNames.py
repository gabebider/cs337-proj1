import json
import re
import spacy
import nltk
#from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.metrics.distance import edit_distance
from nltk.corpus import wordnet
from datetime import datetime
from collections import defaultdict

def truncate_punctuation(text):
    puncSearch = re.search(r":|@|#",text)
    if puncSearch != None:
        text = text[:puncSearch.span()[0]]
    return text

def find_award_array(tweetData):
    # creates spacy model that can do a lot of fancy things
    langProcessor = spacy.load("en_core_web_sm")
    uniqueAwards = defaultdict(int)
    #sia = SentimentIntensityAnalyzer()
    # loop through all our tweets
    for tweet in tweetData:
        # get the text of the tweet
        text = tweet['text']
        # init an empty set to store tweets that we have seen and start with "[bB]est"
        seenTweets = set()
        # find all tweets that mention "best " or "Best " and we havent viewed yet
        bestSearch = re.search(r"\s*[Bb]est .*", text)
        if bestSearch != None and not text in seenTweets:
            # add to set of viewed tweets
            seenTweets.add(text)
            # find the index where the "[Bb]est" starts
            startIndex = int(bestSearch.span()[0])
            # extract the tweet from best to the end
            subTweet = truncate_punctuation(text[startIndex:])
            # load tweet into our classifier and remove trailing/leading white space
            classifiedText = langProcessor(subTweet.strip())
            # loop through the entities of the Doc
            # https://spacy.io/api/doc
            # ents: A list of strings, of the same length of words, to assign the token-based IOB tag. Defaults to None.
            for entity in classifiedText.ents:
                # print(f"Classified Ent: \"{awards.text}\"")
                # see if token has the word best and if so we increase its count by 1
                if re.search(r"\s*[Bb]est .*", entity.text):
                    uniqueAwards[entity.text.strip()] += 1
    finalAwardsArray = []
    # loop through each award that we have found
    for entity, frequency in uniqueAwards.items():
        # if it has at least 1 vote add it to the final array
        if frequency > 1:
            finalAwardsArray.append([ entity, frequency ])
    return finalAwardsArray

def clean_award_array(arr):
    """
        Cleans our final award array by combining similar names

        Parameters
        ----------
        arr : list of lists
            List represnting an award name with its number of votes
            arr[0] = award name
            arr[1] = count of votes
    """
    count = 0
    endPoint = len(arr)
    final_dict = dict()
    nlp = spacy.load("en_core_web_md")
    # iterate through tweets
    while len(arr) > 0 and count < endPoint:
        count = count + 1
        # remove an entry from our awards list
        entry = arr.pop()
        # get the index of the first space
        spaceIndex = entry[0].index(" ") + 1
        # cut off the "Best " part of the tweet
        currentTweet = nlp(entry[0][spaceIndex:])
        # get the count of the current tweet
        currentCount = entry[1]
        # init a boolean to see if we have placed the tweet yet in our final dict
        placed = False
        # iterate through all remaining tweets and check if they are related to current tweet
        for tweets in arr:
            # get the index of the first space (could hardcode this index)
            spaceIndex = tweets[0].index(" ") + 1
            # if the current tweet has more votes than the tweet we are comparing it to and they are not the same tweet
            if currentCount > tweets[1] and not entry[0] == tweets[0]:
                # init a spacy doc for the tweet we are comparing
                comparedTweet = nlp(tweets[0][spaceIndex:])
                # if the similarity between the two tweets is greater than XXXX
                if currentTweet.similarity(comparedTweet) > 0.9:
                    # if we have not placed the tweet yet
                    if not placed:
                        final_dict[entry[0]] = [entry[1] + tweets[1], [(entry[0],entry[1]),(tweets[0],tweets[1])]]
                        # create entry for dict where 
                        # index = [award name, count of votes, [list of tweets]]
                        placed = True
                    else:
                        # add the count of the tweet we are comparing to the index of the entry we just made
                        final_dict[entry[0]][0] += tweets[1]
                        # add the tweet text we are comparing to the list of tweets that are similar
                        final_dict[entry[0]][1].append((tweets[0],tweets[1]))
    
    # print out the final dict
    for name, elements in final_dict.items():
        print(f"{name}: {elements}\n")
    return final_dict

def test():
    # langProcesor = spacy.load("en_core_web_sm")
    # str1 = "Best Motion Picture for Comedy/Musical"
    # str2 = "Best Motion Picture - Musical or Comedy"
    # num = edit_distance(str1, str2)
    # print(num)
    nlp = spacy.load("en_core_web_md")
    doc1 = nlp("Best Motion Picture / Comedy or Musical")
    doc2 = nlp("Best Television Comedy/Musical Series")
    similarity = doc1.similarity(doc2)
    print(similarity)

def get_award_categories():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Find Award Names process started at =", dt_string)
    arr = find_award_array(json.load(open('gg2013.json')))
    # print(arr)
    cleanedArr = clean_award_array(arr)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Find Award Names process ended at =", dt_string)
    return cleanedArr

get_award_categories()