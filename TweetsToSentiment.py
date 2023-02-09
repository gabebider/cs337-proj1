from Award import Award
from AwardCategory import AwardCategory
from TweetsNearMedian import TweetsNearMedian
import re
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
        name1 = award.winner.lower()
        name2 = award.winner.lower().replace(" ", "")
        pattern = f"{name1}|{name2}"
        sentimentCount = 0
        for tweet in currTweets:
            if re.search(pattern, tweet['text'].lower()):
                sentiment = sentiment_analyzer.polarity_scores(tweet['text'])
                sentimentCount = sentimentCount + sentiment["compound"]
        sentimentsDict[award.award_category.award_name] = [award.winner, sentimentCount]
    print(sentimentsDict)
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
    print(sentimentsDict)
    return sentimentsDict

def find_sentiments(tweets, hosts, awardsList):
    nltk.download("vader_lexicon", quiet=True)
    hostSentiment = get_sentiment_hosts(tweets, hosts)
    winnersSentiment = get_sentiments_winners(tweets, awardsList)
    pass