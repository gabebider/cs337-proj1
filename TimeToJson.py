
from TweetsNearMedian import TweetsNearMedian
from utils import preprocess
import os
import json

# This creates some cool plots try it if you have time :)
def run():

    os.system("rm test_tweets_time/*")

    with open("award_aliases.json", "r") as file:
        awards = json.load(file)

    tweets = preprocess(json.load(open(f'gg2013.json')))

    for name,award in awards.items():
        file_name = name.replace(" ","_")
        relevant_tweets = TweetsNearMedian(tweets,award[1],2,3,save_name=file_name)
        # print(len(relevant_tweets))
        jsonob = json.dumps(relevant_tweets, indent = 4)
        with open(f"test_tweets_time/{file_name}.json",'w') as outfile:
            outfile.write(jsonob)

if __name__ == "__main__":
    run()


