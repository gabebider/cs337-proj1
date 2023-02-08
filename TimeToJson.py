from TweetsByTime import Tweets_By_Time
from EliWhat import EliWhat
from utils import preprocess
import json

with open("award_aliases.json", "r") as file:
    awards = json.load(file)

tweets = preprocess(json.load(open(f'gg2013.json')))

for award in awards.values():
    relevant_tweets = EliWhat(tweets,award[1],3,3)
    print(len(relevant_tweets))
    jsonob = json.dumps(relevant_tweets, indent = 4)

    file_name = award[1][0].replace(" ","_")
    with open(f"test_tweets_time/{file_name}.json",'w') as outfile:
        outfile.write(jsonob)
    exit()

