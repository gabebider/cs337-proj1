import logging
from aliases import award_aliases
from utils import standardize
import json
import numpy as np

def Tweets_By_Time(tweets, award_name_aliases, range=0.7):
    '''
    This function returns all tweets that are in the middle ((range))% of tweets that mention the award name with retweets removed
    i.e. it finds all tweets that mention the award name
    it takes the middle ((range))% of those tweets
    it then finds the minimum and maximum time stamp of those tweets
    it then returns all tweets that are between that minimum and maximum time stamp

    Parameters:
        tweets: list of all tweets
        award_name_aliases: list of all names for a single award 
        range: float of range of tweets to return

    Returns:
        list of all tweets in the middle ((range))% of tweets that mention the award name with retweets removed
    '''

    if range > 1 or range < 0:
        raise ValueError("Range must be between 0 and 1")
    
    # remove all retweets
    tweets = [tweet for tweet in tweets if not tweet['text'].startswith('RT ')]

    # find all tweets that mention the award name
    tweets_with_award_name = []
    for tweet in tweets:
        text = tweet['text'].lower()
        for alias in award_name_aliases:
            alias = alias.lower()
            if alias in text:
                tweets_with_award_name.append(tweet)
                break

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
    print(start_time)
    end_time = tweets_with_award_name[end]['timestamp_ms']
    print(end_time)

    # return all tweets that are in the middle ((range))% of tweets that mention the award name

    relevant_tweets = [tweet for tweet in tweets if start_time <= tweet['timestamp_ms'] <= end_time]
    if len(relevant_tweets) < 2:
        logging.warning(f"Only {len(relevant_tweets)} tweets returned for award: {award_name_aliases[0]} when using TweetsByTime.py")
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

