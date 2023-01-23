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


def NomineesToWinner(award, winner, totalCount, noneCount):
    nomineeNameDict = {}
    # print(award)
    # exit()
    for nomineeObject in award['nominees']:
        # print(nominee)
        # exit()
        nomineeNameDict[nomineeObject["nominee"]] = 0
    for item in data:
        text = item['text'].lower()
        for nominee in nomineeNameDict:
            if re.match(r".*"+nominee+".*", text):
                nomineeNameDict[nominee] += 1

    mostPopular = max(nomineeNameDict, key=nomineeNameDict.get)
    # print(f"Most popular nominee for {award}: {mostPopular}")
    # print(award['winner'])
    # exit()
    totalCount += 1
    if award["winner"] is not None and award['winner']['nominee'] == mostPopular:
        return True
    elif award["winner"] is not None:
        print(f"\nMost popular: {mostPopular}")
        print(f"True winner: {award['winner']['nominee']}")
        print(f"Counts: {nomineeNameDict}\n")
        return False
    else:
        print(f"None winner for {winner}")
        noneCount += 1
        return False

        # print(f"Most popular nominee for {winner}: {mostPopular}")


results = []
# print(awards)
# exit()
noneCount = 0
totalCount = 0

for award in awards.keys():
    results.append(NomineesToWinner(awards[award], award, totalCount, noneCount))

print("None count: ", noneCount)
print("Total count: ", totalCount)
print(sum(results)/len(results))
