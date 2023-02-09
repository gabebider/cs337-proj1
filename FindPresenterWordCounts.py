import matplotlib.pyplot as plt
import aliases
import json
from utils import standardize, preprocess
from collections import Counter

tweets = preprocess(json.load(open('gg2013.json')))
tweets = [tweet['text'].lower() for tweet in tweets if not tweet['text'].startswith('RT ')]


presenters = []
data = json.load(open('autograder/gg2013answers.json'))
values = data['award_data'].values()

for value in values:
    for presenter in value['nominees']:
        presenters.append(presenter)

counter = Counter()
stop_words = set({'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will', 'with'})
for tweet in tweets:
    for presenter in presenters:
        if presenter in tweet:
            tokens = tweet.split()
            for token in tokens:
                if token not in stop_words and token not in presenter.split():
                    counter[token] += 1

# sort the counter by value
counter = {k: v for k, v in sorted(counter.items(), key=lambda item: item[1], reverse=True)}

with open("nominee_words.json", "w") as f:
    json.dump(counter, f)
