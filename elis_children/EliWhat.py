import matplotlib.pyplot as plt
import aliases
import json
from utils import standardize

tweets = json.load(open('gg2013.json'))
award_name_aliases = aliases.award_aliases['best television series - drama']
# remove all RTs
tweets = [t for t in tweets if not t['text'].startswith('RT ')]

x_salma = []
y_salma = []
salma_count = 0
x_rudd = []
y_rudd = []
rudd_count = 0
person_1 = "arnold schwarzenegger"
person_2 = "sylvester stallone"
# create a graph that shows tweets vs time
y_v = 0
for tweet in tweets:
    tweet_text = standardize(tweet['text']).lower()
    if person_1 in tweet_text:
        x_salma.append(tweet['timestamp_ms'])
        y_salma.append(salma_count)
        salma_count += 1
    elif person_2 in tweet_text:
        x_rudd.append(tweet['timestamp_ms'])
        y_rudd.append(rudd_count)
        rudd_count += 1

# plt.plot(x_salma, y_salma, label = f'{person_1}')
# plt.plot(x_rudd, y_rudd, label = f'{person_2}')
# plt.legend()
# plt.show()
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
plt.plot(x_alias, y_alias, label = 'Tweets with Award Name')
horizontal_line = len(tweets_with_award_name) * .7
plt.axhline(y = horizontal_line, label = '70% of tweets')

# find median time of tweets with award name
median_time = tweets_with_award_name[int(len(tweets_with_award_name) / 2)]['timestamp_ms']
plt.axvline(x = median_time, label = 'Median Time')

# add 3 minutes to the median time
median_time_plus_3 = median_time + 3 * 60 * 1000
# plot the dashed line
plt.axvline(x = median_time_plus_3, color = 'r', linestyle = '--', label = 'Median Time + 3 minutes')
# subtract 3 minutes from the median time
median_time_minus_3 = median_time - 3 * 60 * 1000
# plot the dashed line
plt.axvline(x = median_time_minus_3, color = 'r', linestyle = '--', label = 'Median Time - 3 minutes')

# sort tweets by time
tweets_with_award_name.sort(key=lambda x: x['timestamp_ms'])



# range = .7
# find the middle ((range))% of tweets from tweets that mention award name
# start = int(len(tweets_with_award_name) * (1 - range) / 2)
# end = int(len(tweets_with_award_name) * (1 + range) / 2)

# if start < 0:
#     start = 0
# if end > len(tweets_with_award_name) - 1:
#     end = len(tweets_with_award_name) - 1

# find the time stamp fo the beginning and end of the middle ((range))% of tweets
# start_time = tweets_with_award_name[start]['timestamp_ms']
# end_time = tweets_with_award_name[end]['timestamp_ms']
# plt.axvline(x = start_time, label = 'start time')
# plt.axvline(x = end_time, color = 'r', label = 'end time')

# tweet_x = []
# tweet_y = []
# y_v = 0
# for tweet in tweets:
#     for alias in award_name_aliases:
#         if alias in standardize(tweet['text']).lower():
#             tweet_x.append(tweet['timestamp_ms'])
#             tweet_y.append(y_v)
#             y_v += 1
#             break

# plt.plot(tweet_x, tweet_y, label='All tweets')

# plt.plot(x, y, label='Tweets with Title')
plt.xlabel('Time')
plt.ylabel('Number of Tweets')
# plt.title('Tweets vs time')
plt.legend()
plt.show()
