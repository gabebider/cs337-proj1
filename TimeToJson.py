from TweetsByTime import Tweets_By_Time
from EliWhat import EliWhat
from utils import preprocess
import os
import json

def run():

    os.system("rm test_tweets_time/*")

    with open("award_aliases.json", "r") as file:
        awards = json.load(file)

    tweets = preprocess(json.load(open(f'gg2013.json')))

    for name,award in awards.items():
        relevant_tweets = EliWhat(tweets,award[1],2,2)
        print(len(relevant_tweets))
        jsonob = json.dumps(relevant_tweets, indent = 4)

        file_name = name.replace(" ","_")
        with open(f"test_tweets_time/{file_name}.json",'w') as outfile:
            outfile.write(jsonob)

if __name__ == "__main__":
    run()


