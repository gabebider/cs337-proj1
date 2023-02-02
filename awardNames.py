import json
import re
import spacy
import nltk
#from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.metrics.distance import edit_distance
from nltk.corpus import wordnet
from datetime import datetime
from collections import defaultdict

def clean_str(text):
    httpSearch = re.search(r"http",text)
    if httpSearch is not None:
        text = text[:httpSearch.span()[0]]
    text = re.sub(r'/',' or ',text)
    text = re.sub(r'- ','',text)
    return re.sub(r'[^A-Za-z\' ]+','',text)

## truncates at the first instance of a part of speech in the pos_array
## if delete is `True`, returns an empty string
def pos_truncate(nlp_model,text,pos_array):
    doc = nlp_model(text)
    truncInd = len(doc)
    for ind, token in enumerate(doc):
        if token.pos_ in pos_array:
            truncInd = ind
            break
    return doc[0:truncInd].text.strip()

def pos_check(nlp_model,text,pos_array,index):
    if text == "":
        return ""
    doc = nlp_model(text)
    if index >= len(doc):
        return text
    return "" if doc[index].pos_ in pos_array else text

def get_first_noun(nlp_model,text):
    doc = nlp_model(text)
    for token in doc:
        if token.pos_ == "NOUN":
            return (text,token.text)
    return ("",None)
    

## prints out the parts of speech of a string
def pos_ify(nlp_model,text):
    doc = nlp_model(text)
    print("\n",text)
    for ind, token in enumerate(doc):
        print(ind,token.text,token.pos_)


def find_award_array(tweetData):
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("merge_entities")
    # nlp.add_pipe("merge_noun_chunks")
    uniqueAwards = defaultdict(int)
    seenTweets = set()
    for tweet in tweetData:
        text = tweet['text'].lower()
        bestSearch = re.search(r"\s[Bb]est .*",text)
        if bestSearch != None and not text in seenTweets:
            seenTweets.add(text)
            startIndex = bestSearch.span()[0]
            subTweet = clean_str(text[startIndex:].strip())

            text = pos_truncate(nlp,subTweet,['PROPN','PRON','VERB','AUX','INTJ','NUM','PART','SCONJ','SYM'])
            text = pos_check(nlp,text,['ADP','AUX','DET','CCONJ'],-1)
            text = pos_check(nlp,text,['ADP','AUX','DET'],1)
            text, firstNoun = get_first_noun(nlp,text)

            if text == "best":
                text = ""

            if text:
                uniqueAwards[text] += 1
    

    finalAwardsArray = []
    # loop through each award that we have found
    for entity, frequency in uniqueAwards.items():
        # if it has at least 1 vote add it to the final array
        if frequency > 1:
            finalAwardsArray.append([ entity, frequency ])
    return finalAwardsArray       


        

# def find_award_array(tweetData):
#     # creates spacy model that can do a lot of fancy things
#     langProcessor = spacy.load("en_core_web_sm")
#     uniqueAwards = defaultdict(int)
#     seenTweets = set()
#     #sia = SentimentIntensityAnalyzer()
#     # loop through all our tweets
#     for tweet in tweetData:
#         # get the text of the tweet
#         text = tweet['text']
#         # init an empty set to store tweets that we have seen and start with "[bB]est"
#         # find all tweets that mention "best " or "Best " and we havent viewed yet
#         bestSearch = re.search(r"\s*[Bb]est .*", text)
#         if bestSearch != None and not text in seenTweets:
#             # add to set of viewed tweets
#             seenTweets.add(text)
#             # find the index where the "[Bb]est" starts
#             startIndex = int(bestSearch.span()[1])
#             # extract the tweet from best to the end
#             subTweet = truncate_punctuation(text[startIndex:])
#             # load tweet into our classifier and remove trailing/leading white space
#             classifiedText = langProcessor(subTweet.strip())
#             # loop through the entities of the Doc
#             # https://spacy.io/api/doc
#             # ents: A list of strings, of the same length of words, to assign the token-based IOB tag. Defaults to None.
#             for entity in classifiedText.ents:
#                 # print(f"Classified Ent: \"{awards.text}\"")
#                 # see if token has the word best and if so we increase its count by 1
#                 if re.search(r"\s*[Bb]est .*", entity.text):
#                     uniqueAwards[entity.text.strip()] += 1
#     finalAwardsArray = []
#     # loop through each award that we have found
#     for entity, frequency in uniqueAwards.items():
#         # if it has at least 1 vote add it to the final array
#         if frequency > 1:
#             finalAwardsArray.append([ entity, frequency ])
#     return finalAwardsArray

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
                        final_dict[entry[0]] = [entry[1] + tweets[1], [entry[0],tweets[0]]]
                        # create entry for dict where 
                        # index = [award name, count of votes, [list of tweets]]
                        placed = True
                    else:
                        # add the count of the tweet we are comparing to the index of the entry we just made
                        final_dict[entry[0]][0] += tweets[1]
                        # add the tweet text we are comparing to the list of tweets that are similar
                        final_dict[entry[0]][1].append(tweets[0])
    
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