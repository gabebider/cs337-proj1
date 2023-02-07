'''
This file is meant to find the middle ((range))% of tweets that mention a given award name
'''
from aliases import award_aliases
from utils import standardize
import json
import numpy as np

def Tweets_By_Time(tweets, award_name_aliases, range=.9):
    '''
    Parameters:
        tweets: list of all tweets
        award_name_aliases: list of all names for a single award 
        range: float of range of tweets to return

    Returns:
        list of all tweets in the middle ((range))% of tweets that mention the award name
    '''

    if range > 1 or range < 0:
        raise ValueError("Range must be between 0 and 1")

    # remove all tweets with the same text
    seen_tweets = set()
    unique_tweets = []
    for tweet in tweets:
        if tweet['text'] not in seen_tweets:
            seen_tweets.add(tweet['text'])
            unique_tweets.append(tweet)
    
    tweets = unique_tweets

    # find all tweets that mention the award name
    tweets_with_award_name = []
    for tweet in tweets:
        text = standardize(tweet['text'].lower())
        for alias in award_name_aliases:
            alias = standardize(alias)
            if alias in text:
                tweets_with_award_name.append(tweet)
                break

    # remove any retweets
    tweets_with_award_name = [tweet for tweet in tweets_with_award_name if not tweet['text'].startswith('RT ')]
    # sort tweets by time
    tweets_with_award_name.sort(key=lambda x: x['timestamp_ms'])

    # find the middle ((range))% of tweets from tweets that mention award name
    start = int(len(tweets_with_award_name) * (1 - range) / 2)
    end = int(len(tweets_with_award_name) * (1 + range) / 2)
    if start < 0:
        start = 0
    if end > len(tweets_with_award_name) - 1:
        end = len(tweets_with_award_name) - 1

    # find the time stamp fo the beginning and end of the middle ((range))% of tweets
    start_time = tweets_with_award_name[start]['timestamp_ms']
    end_time = tweets_with_award_name[end]['timestamp_ms']

    # return all tweets that are in the middle ((range))% of tweets that mention the award name

    relevant_tweets = [tweet for tweet in tweets if start_time <= tweet['timestamp_ms'] <= end_time]
    return relevant_tweets

if __name__ == '__main__':
    tweets_by_time = Tweets_By_Time(json.load(open('gg2013.json')), award_aliases['best performance by an actress in a motion picture - drama'])
    # print(tweets_by_time)
    # print("The length of the tweets_by_time list is: ", len(tweets_by_time))
    
    # some code to try to find the optimal range
    # floats_list = np.arange(0, 1.00, 0.02).tolist()
    # length_of_tweets = []
    # for range in floats_list:
    #     print(f"Finding tweets for range: {range}")
    #     tweets_by_time = Tweets_By_Time(json.load(open('gg2013.json')), award_aliases['best performance by an actress in a motion picture - drama'], range)
    #     length_of_tweets.append( (range, len(tweets_by_time)) )

    # x, y = zip(*length_of_tweets)
    # plt.plot(x, y)
    # plt.xlabel('Range')
    # plt.ylabel('Len of list returned')
    # plt.title('Tweets returned vs range')

    # # Showing the plot
    # plt.show()

