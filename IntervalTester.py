import matplotlib.pyplot as plt
from Award import Award
import json
import numpy as np
from utils import standardize, preprocess

## more fun graphs
def TweetsNearMedian(tweets,award_name_aliases,min_before,min_After,save_name=""):
    # remove all RTs
    tweets = [t for t in tweets if not t['text'].startswith('RT ')]
    tweets = [tweet for tweet in tweets if "http" not in tweet['text']]

    tweets_with_award_name = []
    for tweet in tweets:
        text = tweet['text'].lower()
        for alias in award_name_aliases:
            alias = alias.lower()
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

    # horizontal_line = len(tweets_with_award_name) * .7
    # plt.axhline(y = horizontal_line, label = '70% of tweets')

    # # find median time of tweets with award name
    # print(len(tweets_with_award_name))
    if len(tweets_with_award_name) == 0:
        print(f"No tweets with award name {award_name_aliases[0]}")
        return [], 0, 0, 0
    median_time = tweets_with_award_name[int(len(tweets_with_award_name) / 2)]['timestamp_ms']

    # # add 3 minutes to the median time
    end_time = median_time + (min_After * 60 * 1000)
    
    # # subtract 3 minutes from the median time
    start_time = median_time - (min_before * 60 * 1000)

    # if award_name_aliases[0] == "best actor drama":
    #     print(f"Median Time: {median_time}")
    #     print(f"{min_after} * 60 * 1000: {min_After * 60 * 1000}")
    #     print(f"end_time: {end_time}")
    
    relevant_tweets = [tweet for tweet in tweets if start_time <= tweet['timestamp_ms'] <= end_time] 

    if save_name != "":
        plt.plot(x_alias, y_alias, label = 'Tweets with Award Name')
        plt.axvline(x = median_time, label = 'Median Time')
        plt.axvline(x = end_time, color = 'r', linestyle = '--', label = f'Median Time + {min_After} minutes')
        plt.axvline(x = start_time, color = 'r', linestyle = '--', label = f'Median Time - {min_before} minutes')
        plt.xlabel('Time')
        plt.ylabel('Number of Tweets')
        plt.title('Tweets vs time')
        plt.legend()
        plt.savefig(f"test_tweets_time/{save_name}.png")
        plt.close()
        # plt.show()
    return relevant_tweets, median_time, start_time, end_time

if __name__ == "__main__":
    from matplotlib.legend_handler import HandlerTuple
    tweets = preprocess(json.load(open('gg2013.json')))
    awards = json.load(open('award_aliases.json'))
    award_aliases = []
    for award in awards:
        aliases = awards[award][1] 
        award_aliases.append(aliases)

    
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'aliceblue', 'antiquewhite', 'aqua', 
          'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 
          'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 
          'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 
          'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 
          'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 
          'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 
          'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 
          'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 
          'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 
          'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 
          'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 
          'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 
          'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 
          'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 
          'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 
          'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 
          'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 
          'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 
          'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 
          'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 
          'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 
          'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 
          'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 
          'springgreen']
    interval_times = []
    overlap_counts = []
    for time in [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1, 1.5, 2, 2.5, 3]:
        color_index = 0
        all_intervals = []
        for alias_list in award_aliases:
            min_before = time
            min_after = time
            tweets_near_median, median_time, start_time, end_time = TweetsNearMedian(tweets,alias_list,min_before, min_after)
            all_intervals.append( (start_time, end_time) )
            # plt.axvline(x = start_time, label = f"{alias_list[0]}", linestyle = 'dashed', color = colors[color_index])
            # plt.axvline(x = end_time, label = f"{alias_list[0]}", linestyle = 'dashed', color = colors[color_index])
            color_index += 1

        # find number of intervals that overlap in all_intervals
        START = 0
        END = 1
        overlap_count = 0
        overlappers = []
        for inteval_1 in all_intervals:
            for inteval_2 in all_intervals:
                if inteval_1 != inteval_2:
                    if inteval_1[START] < inteval_2[START] < inteval_1[END] and (inteval_2, inteval_1) not in overlappers:
                        # print(f"Overlap: {inteval_1} and {inteval_2}")
                        overlap_count += 1
                        overlappers.append((inteval_1, inteval_2))
                    elif inteval_2[START] < inteval_1[START] < inteval_2[END] and (inteval_2, inteval_1) not in overlappers:
                        # print(f"Overlap: {inteval_1} and {inteval_2}")
                        overlap_count += 1
                        overlappers.append((inteval_1, inteval_2))
        print(f"Number of overlaps when min_before and min_after are {time}: {overlap_count}")
        interval_times.append(time)
        overlap_counts.append(overlap_count)
        
    plt.plot(interval_times, overlap_counts, label = 'Number of Overlaps')
    tweet_times = []
    tweet_y = []
    tweet_count = 0
    for tweet in tweets:
        tweet_times.append(tweet['timestamp_ms'])
        tweet_y.append(tweet_count)
        tweet_count += 1
    # plt.plot(tweet_times, tweet_y, label = 'All Tweets')
    # plt.legend()
    plt.show()


