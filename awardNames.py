import json
import re
import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime

def find_award_array(tweetData):
    langProcesor = spacy.load("en_core_web_sm")
    awardsArray = []
    sia = SentimentIntensityAnalyzer()
    for tweet in tweetData:
        text = tweet['text']
        tweetArray = []
        if re.search(r"\s*[Bb]est .*", text) and not text in tweetArray:
            tweetArray.append(text)
            sentiment = sia.polarity_scores(text)
            if sentiment['compound'] > 0:
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
    print(arr)
    pass

def test():
    nlp = spacy.load("en_core_web_md")
    doc1 = nlp("Best Motion Picture / Comedy or Musical")
    doc2 = nlp("Best Television Comedy/Musical Series")
    similarity = doc1.similarity(doc2)
    print(similarity)

def get_award_categories():
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # print("Find Award Names process started at =", dt_string)
    # arr = find_award_array(json.load(open('gg2013.json')))
    # cleanedArr = clean_award_array(arr)
    test()
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # print("Find Award Names process ended at =", dt_string)

get_award_categories()