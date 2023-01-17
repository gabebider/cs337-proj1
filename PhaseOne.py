import pprint
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import re
import nltk
import csv

from Nominees import getNominees
nltk.download('vader_lexicon')

data = json.load(open('gg2013.json'))

djangoCount = 0
argoCount = 0
printCount = 0
sia = SentimentIntensityAnalyzer()

awards = getNominees()


def testAward(award):
    nomineeNameDict = {}
    for nominee in award['nominees']:
        nomineeNameDict[nominee] = 0
    for item in data:
        text = item['text'].lower()
        for nominee in nomineeNameDict:
            if re.match(r".*"+nominee+".*", text):
                nomineeNameDict[nominee] += 1

    mostPopular = max(nomineeNameDict, key=nomineeNameDict.get)
    # print(f"Most popular nominee for {award}: {mostPopular}")
    if award['winner']['nominee'] == mostPopular:
        return True
    else:
        return False


results = []
for award in awards:
    results.append(testAward(award))

print(sum(results)/len(results))
