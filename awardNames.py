import json
import re
import spacy
import nltk
#from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.metrics.distance import edit_distance
from nltk.corpus import wordnet
from datetime import datetime

def find_award_array(tweetData):
    langProcesor = spacy.load("en_core_web_sm")
    awardsArray = []
    #sia = SentimentIntensityAnalyzer()
    for tweet in tweetData:
        text = tweet['text']
        tweetArray = []
        if re.search(r"\s*[Bb]est .*", text) and not text in tweetArray:
            tweetArray.append(text)
            #sentiment = sia.polarity_scores(text)
            #if sentiment['compound'] > -2:
            index = re.search(r"\s*[Bb]est .*", text).span()
            subTweet = text[int(index[0]):]
            classifiedText = langProcesor(subTweet.strip())
            for awards in classifiedText.ents:
                if re.search(r"\s*[Bb]est .*", awards.text):
                    found = False
                    for arrIndex in range(len(awardsArray)):
                        if awards.text == awardsArray[arrIndex][0]:
                            awardsArray[arrIndex][1] = awardsArray[arrIndex][1] + 1
                            found = True
                    if found == False:
                        awardsArray.append([awards.text.strip(), 1])
    finalAwardsArray = []
    for arrIndex in range(len(awardsArray)):
        if awardsArray[arrIndex][1] > 1:
            finalAwardsArray.append(awardsArray[arrIndex])
    return finalAwardsArray

def clean_award_array(arr):
    final_array = dict()
    nlp = spacy.load("en_core_web_md")
    index = 0
    while len(arr) > 0:
        entry = arr.pop(0)
        currentTweet = nlp(entry[0])
        currentCount = entry[1]
        placed = False
        for tweets in arr:
            if currentCount > tweets[1]:
                comparedTweet = nlp(tweets[0])
                if currentTweet.similarity(comparedTweet) > 0.85:
                    if placed == False:
                        index = index + 1
                        final_array[index] = [entry[0], entry[1] + tweets[1], [tweets[0]]]
                        placed = True
                    else:
                        final_array[index][1] = final_array[index][1] + tweets[1]
                        final_array[index][2].append(tweets[0])
        # if placed == False:
        #     arr.append(entry)
    print(final_array)
    pass

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
    cleanedArr = clean_award_array(arr)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Find Award Names process ended at =", dt_string)
    #test()

get_award_categories()