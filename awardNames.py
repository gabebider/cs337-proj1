import json
import re
import spacy

def find_award_names(tweetData):
    langProcesor = spacy.load("en_core_web_sm")
    awardsArray = []
    for tweet in tweetData:
        text = tweet['text']
        tweetArray = []
        if re.search(r"\s*[Bb]est .*", text) and not text in tweetArray:
            tweetArray.append(text)
            index = re.search(r"\s*[Bb]est .*", text).span()
            subTweet = text[int(index[0]):]
            while subTweet[0].isspace():
                subTweet = subTweet[1:]
            classifiedText = langProcesor(subTweet)
            for awards in classifiedText.ents:
                if re.search(r"\s*[Bb]est .*", awards.text):
                    found = False
                    for arrIndex in range(len(awardsArray)):
                        if awards.text == awardsArray[arrIndex][0]:
                            awardsArray[arrIndex][1] = awardsArray[arrIndex][1] + 1
                            found = True
                    if found == False:
                        awardsArray.append([awards.text, 1])
    finalAwardsArray = []
    for arrIndex in range(len(awardsArray)):
        if awardsArray[arrIndex][1] > 1:
            finalAwardsArray.append(awardsArray[arrIndex])
    print(finalAwardsArray)

find_award_names(json.load(open('gg2013.json')))