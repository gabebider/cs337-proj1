import logging
from aliases import award_aliases
from utils import standardize
import json
import numpy as np

def FirstXPercent(tweets, award_name_aliases, percent:float=0.3):
    '''
    This function returns all tweets that are in the first ((percent))% of tweets that mention the award name with retweets removed
    i.e. it finds all tweets that mention the award name
    it takes the first ((percent))% of those tweets
    it then finds the minimum and maximum time stamp of those tweets
    it then returns all tweets that are between that minimum and maximum time stamp

    Parameters:
        tweets: list of all tweets
        award_name_aliases: list of all names for a single award 
        percent: float of range of tweets to return

    Returns:
        list of all tweets in the first ((percent))% of tweets that mention the award name with retweets removed
    '''

    if percent > 1 or percent < 0:
        raise ValueError("Range must be between 0 and 1")
    
    # remove all retweets
    tweets = [tweet for tweet in tweets if not tweet['text'].startswith('RT ')]

    # find all tweets that mention the award name
    tweets_with_award_name = []
    for tweet in tweets:
        text = standardize(tweet['text']).lower()
        for alias in award_name_aliases:
            alias = standardize(alias).lower()
            if alias in text:
                tweets_with_award_name.append(tweet)
                break

    # sort tweets by time
    tweets_with_award_name.sort(key=lambda x: x['timestamp_ms'])

    # find the first ((range))% of tweets from tweets that mention award name
    start = 0
    end = int(len(tweets_with_award_name) * percent)
    if start < 0:
        start = 0
    if end > len(tweets_with_award_name) - 1:
        end = len(tweets_with_award_name) - 1

    # find the time stamp fo the beginning and end of the middle ((range))% of tweets
    start_time = tweets_with_award_name[start]['timestamp_ms']
    end_time = tweets_with_award_name[end]['timestamp_ms']

    # return all tweets that are in the first ((percent))))% of tweets that mention the award name

    relevant_tweets = [tweet for tweet in tweets if start_time <= tweet['timestamp_ms'] <= end_time]
    if len(relevant_tweets) < 2:
        logging.warning(f"Only {len(relevant_tweets)} tweets returned for award: {award_name_aliases[0]} when using TweetsByTime.py")

    return relevant_tweets

if __name__ == '__main__':
    tweets_by_time = FirstXPercent(json.load(open('gg2013.json')), award_aliases['best performance by an actress in a motion picture - drama'])