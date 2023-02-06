from Award import Award
import csv
from AwardCategory import AwardCategory
from collections import Counter
from aliases import get_aliases
from utils import standardize
from TweetsByTime import Tweets_By_Time
import json
import spacy
import re
from collections import defaultdict

# def getAwards():
#     awards = []
#     addedAwards = []
#     aliases = get_aliases()

#     # create list of awards
#     for cat in aliases:
#         if cat not in addedAwards:
#             addedAwards.append(cat)
#             awardStruct = Award(AwardCategory(cat))
#             awardStruct.award_category.aliases = aliases[cat]
#             awards.append(awardStruct)
#     return awards

def AwardNameToWinners(tweets, award):
    '''
    Function to go from award names to winners
    Returns a list of updated Award objects with the winner field filled in

    Parameters
    ----------
    tweets : list[dict] (not sure if this is the right type, but the json file opened yknow)
    award : Award (the award we are trying to find the winner for)

    Returns
    -------
    winner : str (the name of the winner)

    '''
    # check type constraints
    if not isinstance(award, Award):
        raise TypeError("award_names must be a list")

    # remove all duplicate tweets
    unique_tweets = []
    unique_text = set()
    for tweet in tweets:
        text = standardize(tweet['text'].lower())
        if text not in unique_text:
            unique_text.add(text)
            unique_tweets.append(tweet)
    # now we have a set of unique tweets to work with
    tweets = unique_tweets

    def get_csv_set(csv_file):
        csvSet = set()
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                for name in row:
                    csvSet.add(name.lower())
        return csvSet
    
    actors_set = get_csv_set("actors.csv")
    movies_set = get_csv_set("movies.csv")

    # standarize a lot
    def ultra_standardize(text):
        text = standardize(text)
        text = text.replace(".", "")
        text = text.replace(",", "")
        text = text.replace("!", "")
        text = text.replace("?", "")
        text = text.replace("@", "")
        text = text.replace("\"", "")
        text = text.replace("-", " ")
        text = text.lower()
        text = text.replace(" has ", "")
        return text

    # helper function to check for "X" won "Y" pattern
    def check_for_won_pattern(award_alias, tweet, award):
        if not isinstance(award_alias, str):
            raise TypeError("award_alias must be a string")
        if not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        if not isinstance(award, Award):
            raise TypeError("award must be an Award object")
        
        if award_alias in tweet and re.search(r" [Ww]on ", tweet):
            try:
                won_index = tweet.lower().split().index("won")
            except:
                pass
            # "X" should be the name of the winner
            # "Y" should be the award name
            # so we will go backward from won_index and keep all those
            for i in range(won_index - 1, -1, -1):
                # append words from i to won_index to the list of canidates
                canidate = ""
                for j in range(i, won_index):
                    canidate += tweet.split()[j] + " "
                canidate = canidate.strip()
                award_winner_canidates.append(canidate)

    # helper function to check for "X" wins "Y" pattern
    def check_for_wins_pattern(award_alias, tweet, award):
        if not isinstance(award_alias, str):
            raise TypeError("award_alias must be a string")
        if not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        if not isinstance(award, Award):
            raise TypeError("award must be an Award object")

        # this covers the "X" wins "Y" case
        # where "X" is the winner and "Y" is the award
        if award_alias in tweet and re.search(r" [Ww]ins ", tweet):
            try:
                wins_index = tweet.lower().split().index("wins")
            except:
                return
            # we will go backward
            for i in range(wins_index - 1, -1, -1):
                canidate = ""
                for j in range(i, wins_index):
                    canidate += tweet.split()[j] + " "
                canidate = canidate.strip()
                award_winner_canidates.append(canidate)

    # helper function to check for "X" goes to "Y" pattern
    def check_for_goes_to_pattern(award_alias, tweet, award):
        if not isinstance(award_alias, str):
            raise TypeError("award_alias must be a string")
        if not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        if not isinstance(award, Award):
            raise TypeError("award must be an Award object")

        # this covers the "X" goes to "Y" case
        # where "X" is the award name and "Y" is the winner
        if award_alias in tweet and re.search(r" [Gg]oes to ", tweet):
            try:
                goes_to_index = tweet.lower().split().index("goes")
            except:
                return
            if goes_to_index + 2 > len(tweet.split()):
                return
            # add all the canidates after "goes to"
            for i in range(goes_to_index + 2, len(tweet.split())):
                canidate = ""
                for j in range(goes_to_index + 2, i + 1):
                    canidate += tweet.split()[j] + " "
                canidate = canidate.strip()
                award_winner_canidates.append(canidate)
            

    award_winner_canidates = []
    # create a dictionary to store canidate answers
    # loop through all tweets
    for tweet in tweets:
        # just the text please
        tweet = ultra_standardize(tweet['text'])
        # loop through all awards
        # check all aliases for award names
        for alias in award.award_category.aliases:
            alias = ultra_standardize(alias)
            # check for the "X" won "Y" pattern
            check_for_won_pattern(alias, tweet, award)
            check_for_goes_to_pattern(alias, tweet, award)
            check_for_wins_pattern(alias, tweet, award)

    # now we have a dictionary of canidates for each award
    # go through each canidate for an award and find the most common
    # this picks the most common canidate and breaks ties by picking the longest string (in hopes of getting full name versus just first or last)
    # winner = max(award_winner_canidates, key=lambda x: (award_winner_canidates.count(x), len(x)))
    candidate_counts = Counter(award_winner_canidates)
    top_twenty = candidate_counts.most_common(20)
    if len(candidate_counts) == 0:
        winner = "No winner found"
        award.winner = winner
    else:
        found = False
        if award.award_category.isPerson:
            for candidate, count in top_twenty:
                if candidate in actors_set:
                    winner = candidate
                    found = True
                    break
        else:
            for candidate, count in top_twenty:
                if candidate in movies_set:
                    winner = candidate
                    found = True
                    break
        if not found:
            winner = top_twenty[0][0]

    return winner
    