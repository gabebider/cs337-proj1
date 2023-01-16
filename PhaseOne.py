from nltk.sentiment import SentimentIntensityAnalyzer
import json
import re
import nltk
nltk.download('vader_lexicon')

data = json.load(open('gg2013.json'))

djangoCount = 0
argoCount = 0
printCount = 0
sia = SentimentIntensityAnalyzer()

movieNameDict = {"life of pi": 0, "lincoln": 0,
                 "zero dark thirty": 0, "django unchained": 0, "argo": 0}

for item in data:
    text = item['text'].lower()
    for movie in movieNameDict:
        if re.match(r".*"+movie+".*", text):
            # print(item['text'])
            # if sia.polarity_scores(item['text'])['compound'] > 0.8:
            # print(item['text'])
            # printCount += 1
            movieNameDict[movie] += 1


print(f"Life of Pi: {movieNameDict['life of pi']}")
print(f"Lincoln: {movieNameDict['lincoln']}")
print(f"Zero Dark Thirty: {movieNameDict['zero dark thirty']}")
print(f"Django Unchained: {movieNameDict['django unchained']}")
print(f"Argo: {movieNameDict['argo']}")
