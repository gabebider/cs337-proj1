from Award import Award
from AwardCategory import AwardCategory
from TweetsNearMedian import TweetsNearMedian
import re
import math
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import json

# Finds the general sentiments around the winners of the awards
def get_sentiments_winners(tweets, awardsList):
    nltk.download("vader_lexicon", quiet=True)
    sentiment_analyzer = SentimentIntensityAnalyzer()
    sentimentsDict = dict()
    for award in awardsList:
        currTweets = TweetsNearMedian(tweets, award.award_category.aliases, 2, 2)
        currTweets = [tweet['text'].lower().replace("best","") for tweet in currTweets]
        name1 = award.winner.lower()
        name2 = award.winner.lower().replace(" ", "")
        pattern = f"{name1}|{name2}"
        sentimentCount = 0
        for tweet in currTweets:
            if re.search(pattern, tweet):
                sentiment = sentiment_analyzer.polarity_scores(tweet)
                sentimentCount = sentimentCount + sentiment["compound"]
        sentimentsDict[award.award_category.award_name] = [award.winner, sentimentCount]
    return sentimentsDict

# Finds the general sentiments around the hosts
def get_sentiment_hosts(tweets, hosts):
    sentimentsDict = dict()
    sentiment_analyzer = SentimentIntensityAnalyzer()
    for host in hosts:
        name1 = host.lower()
        name2 = host.lower().replace(" ", "")
        pattern = f"{name1}|{name2}"
        sentimentCount = 0
        for tweet in tweets:
            if re.search(pattern, tweet['text'].lower()):
                sentiment = sentiment_analyzer.polarity_scores(tweet['text'])
                sentimentCount = sentimentCount + sentiment["compound"]
        sentimentsDict[host] = sentimentCount
    return sentimentsDict

def find_sentiments(tweets, hosts, awardsList):
    results = dict()
    nltk.download("vader_lexicon", quiet=True)
    hostSentiment = get_sentiment_hosts(tweets, hosts)
    for host in hostSentiment:
        if hostSentiment[host] < 0:
            results[host] = "The general sentiment of host " + host + " was negative, with a sentiment score of " + str(hostSentiment[host])
        else:
            results[host] = "The general sentiment of host " + host + " was positive, with a sentiment score of " + str(hostSentiment[host])
    winnersSentiment = get_sentiments_winners(tweets, awardsList)
    bestSent = 0
    bestName = ""
    worstName = ""
    worstSent = math.inf
    # find the highest and lowest sentiments regarding people's outfits
    for winners in winnersSentiment:
        if winnersSentiment[winners][1] > bestSent:
            bestSent = winnersSentiment[winners][1]
            bestName = winnersSentiment[winners][0]
        elif winnersSentiment[winners][1] < worstSent:
            worstSent = winnersSentiment[winners][1]
            worstName = winnersSentiment[winners][0]
    results[bestName] = "The best sentiment from tweeters was for winner " + bestName.capitalize() + " with a sentiment score of " + str(bestSent)
    results[worstName] = "The worst sentiment from tweeters was for winner " + worstName.capitalize() + " with a sentiment score of " + str(worstSent)
    return results