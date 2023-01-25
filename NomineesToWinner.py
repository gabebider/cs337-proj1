import json
import re
import nltk
from unidecode import unidecode
from Nominees import getNominees
nltk.download('vader_lexicon')

data = json.load(open('gg2013.json'))

awards = getNominees()


def NomineesToWinner(award, winner, totalCount, noneCount):
    nomineeNameDict = {}
    tweetDict = {}
    # add all nominees to the nomineeNameDict with a count of 0
    for nomineeObject in award['nominees']:
        nomineeNameDict[nomineeObject["nominee"]] = 0
    # iterate through tweets
    for item in data:
        # remove accents from tweet
        text = unidecode(item['text']).lower()
        if text in tweetDict:
            # skip duplicate tweets
            continue
        else:
            # add to tweet dict
            tweetDict[text] = 1
        for nominee in nomineeNameDict:
            # remove accents from nominee
            normalizedNominee = unidecode(nominee).lower()
            # check if tweet is related to nominee and discusses "win", "won", "winner", or "winning"
            # the "\b" is a word boundary meaning that the word must be a whole word
            if re.search(r".*"+normalizedNominee+".*", text) and re.search(r'\bwin\b|\bwon\b|\bwinner\b|\bwinning\b', text):
                nomineeNameDict[nominee] += 1

    # check if there were no votes for any nominees
    if sum(nomineeNameDict.values()) == 0:
        print(f"No votes were recorded for any nominees for {winner}")
        print(f"True winner: {award['winner']['nominee']}")
        print(f"Counts: {nomineeNameDict}\n")
        totalCount += 1
        return False
    # get the nominee with the most votes
    mostPopular = max(nomineeNameDict, key=nomineeNameDict.get)
    # increment amount of awards that were correctly predicted so we can later find out average
    totalCount += 1
    # check if the winner is the nominee with the most votes
    if award["winner"] is not None and award['winner']['nominee'] == mostPopular:
        return True
    # check if there was no winner or the winner was wrong
    elif award["winner"] is not None:
        print(f"\nMost popular: {mostPopular}")
        print(f"True winner: {award['winner']['nominee']}")
        print(f"Counts: {nomineeNameDict}\n")
        return False
    else:
        print(f"None winner for {winner}")
        noneCount += 1
        return False

results = []
noneCount = 0
totalCount = 0

# iterate through awards and get the winner for each
for award in awards.keys():
    results.append(NomineesToWinner(awards[award], award, totalCount, noneCount))

# print results
print("None count: ", noneCount)
print("Total count: ", totalCount)
print(sum(results)/len(results))
