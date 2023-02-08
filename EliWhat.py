import matplotlib.pyplot as plt
from Award import Award
import json
import numpy as np
from utils import standardize

def EliWhat(tweets,award_name_aliases,minBefore,minAfter):
    # remove all RTs
    tweets = [t for t in tweets if not t['text'].startswith('RT ')]
    tweets = [tweet for tweet in tweets if "http" not in tweet['text']]

    # x_salma = []
    # y_salma = []
    # salma_count = 0
    # x_rudd = []
    # y_rudd = []
    # rudd_count = 0
    # person_1 = "arnold schwarzenegger"
    # person_2 = "sylvester stallone"
    # # create a graph that shows tweets vs time
    # y_v = 0
    # for tweet in tweets:
    #     tweet_text = standardize(tweet['text']).lower()
    #     if person_1 in tweet_text:
    #         x_salma.append(tweet['timestamp_ms'])
    #         y_salma.append(salma_count)
    #         salma_count += 1
    #     elif person_2 in tweet_text:
    #         x_rudd.append(tweet['timestamp_ms'])
    #         y_rudd.append(rudd_count)
    #         rudd_count += 1

    # plt.plot(x_salma, y_salma, label = f'{person_1}')
    # plt.plot(x_rudd, y_rudd, label = f'{person_2}')


    tweets_with_award_name = []
    for tweet in tweets:
        text = standardize(tweet['text']).lower()
        for alias in award_name_aliases:
            alias = standardize(alias).lower()
            if alias in text:
                tweets_with_award_name.append(tweet)
                break


    x_alias = []
    y_alias = []
    alias_count = 0
    for tweet in tweets_with_award_name:
        x_alias.append(tweet['timestamp_ms'])
        y_alias.append(alias_count)
        alias_count += 1

    # plt.plot(x_alias, y_alias, label = 'Tweets with Award Name')
    # horizontal_line = len(tweets_with_award_name) * .7
    # plt.axhline(y = horizontal_line, label = '70% of tweets')

    # # find median time of tweets with award name
    median_time = tweets_with_award_name[int(len(tweets_with_award_name) / 2)]['timestamp_ms']
    # plt.axvline(x = median_time, label = 'Median Time')

    # # add 3 minutes to the median time
    end = median_time + minAfter * 60 * 1000
    # # plot the dashed line
    # plt.axvline(x = median_time_plus_2, color = 'r', linestyle = '--', label = 'Median Time + 3 minutes')
    # # subtract 3 minutes from the median time
    start = median_time - minBefore * 60 * 1000
    # # plot the dashed line
    # plt.axvline(x = median_time_minus_4, color = 'r', linestyle = '--', label = 'Median Time - 3 minutes')
    relevant_tweets = [tweet for tweet in tweets if start <= tweet['timestamp_ms'] <= end] 
    return relevant_tweets
    # plt.xlabel('Time')
    # plt.ylabel('Number of Tweets')
    # # plt.title('Tweets vs time')
    # plt.legend()
    # plt.show()
