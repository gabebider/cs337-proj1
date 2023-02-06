import json
import re
from collections import Counter
from Award import Award
from AwardCategory import AwardCategory
from datetime import datetime
from collections import defaultdict
from aliases import award_aliases, get_aliases
from utils import standardize, build_iterative_regex

def AwardNameToNominees(tweets, award):
    '''
    Finds the nominees for each award category

    Parameters
    ----------
    tweets : list[dict] (not sure if this is the right type, but the json file opened yknow)
    award : Award (the award we are trying to find the nominees for)

    Returns
    -------
    nominees : list[str] (the names of the nominees)
    '''
    if not isinstance(award, Award):
        raise TypeError("award must be a list")

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

    # helper function to check for "X" wins "Y" pattern
    def check_for_should_win_pattern(award_alias, tweet, award):
        if not isinstance(award_alias, str):
            raise TypeError("award_alias must be a string")
        if not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        if not isinstance(award, Award):
            raise TypeError("award must be an Award object")

        # this covers the "X" should win "Y" case
        # where "X" is the nominee and "Y" is the award
        if award_alias in tweet and re.search(r" should win ", tweet):
            try:
                nominated_index = tweet.lower().split().index("should")
            except:
                return
            for i in range(nominated_index - 1, -1, -1):
                nominee = ""
                for j in range(i, nominated_index):
                    nominee += tweet.split()[j] + " "
                nominee = nominee.strip()
                nominee_canidates.append(nominee)

    def check_for_pattern(award_alias, tweet, award, pattern, forward: bool):
        if not isinstance(forward, bool):
            raise TypeError("forward must be a boolean")
        if not isinstance(award_alias, str):
            raise TypeError("award_alias must be a string")
        if not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        if not isinstance(award, Award):
            raise TypeError("award must be an Award object")
        
        if award_alias in tweet and re.search( rf" {pattern} ", tweet):
            # TODO: add try except here 
            if len(pattern.split()) > 1 and forward:
                nominated_index = tweet.lower().split().index(pattern.split()[-1])
            elif len(pattern.split()) > 1 and not forward:
                nominated_index = tweet.lower().split().index(pattern.split()[0])
            else:
                nominated_index = tweet.lower().split().index(pattern)

            if forward:
                for i in range(nominated_index + 1, len(tweet.split())):
                    nominee = ""
                    for j in range(nominated_index + 1, i + 1):
                        nominee += tweet.split()[j] + " "
                    nominee = nominee.strip()
                    nominee_canidates.append(nominee)
            else:
                for i in range(nominated_index - 1, -1, -1):
                    nominee = ""
                    for j in range(i, nominated_index):
                        nominee += tweet.split()[j] + " "
                    nominee = nominee.strip()
                    nominee_canidates.append(nominee)
        
    
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

    nominee_canidates = []
    tracker = 0
     # loop through all tweets
    for tweet in tweets:
        # if tracker % 5000 == 0:
        #     print(f"Looking at tweet {tracker} of {len(tweets)}")
        # tracker += 1
        
        # just the text please
        tweet = ultra_standardize(tweet['text'])
        # check all aliases for award names
        for alias in award.award_category.aliases:
            alias = ultra_standardize(alias)
            check_for_pattern(alias, tweet, award, "should win", False)
            check_for_pattern(alias, tweet, award, "should have won", False)
            check_for_pattern(alias, tweet, award, "should have been", True)
            check_for_pattern(alias, tweet, award, "should have gotten", False)
            check_for_pattern(alias, tweet, award, "robbed", False)
            check_for_pattern(alias, tweet, award, "was robbed", False)
            check_for_pattern(alias, tweet, award, "was nominated for", False)
            check_for_pattern(alias, tweet, award, "is nominated for", False)
            check_for_pattern(alias, tweet, award, "nominees are", True)
            check_for_pattern(alias, tweet, award, "lost", False)
            check_for_pattern(alias, tweet, award, "to win", False)
            check_for_pattern(alias, tweet, award, "should have been", True)
            check_for_pattern(alias, tweet, award, "deserved", False)
            check_for_pattern(alias, tweet, award, "deserves", False)
            
            # check_for_goes_to_pattern(alias, tweet, award)
            # check_for_wins_pattern(alias, tweet, award)

    candidate_counts = Counter(nominee_canidates)
    top_five = candidate_counts.most_common(5)
    if len(top_five) == 0:
        nominees = "No winner found"
        award.nominees = [nominees]
    else:
        award.nominees = top_five
    # print(nominee_canidates)

    return top_five
            


def getAwards():
    awards = []
    addedAwards = []
    aliases = get_aliases()

    # create list of awards
    for cat in aliases:
        if cat not in addedAwards:
            addedAwards.append(cat)
            awardStruct = Award(AwardCategory(cat))
            awardStruct.award_category.aliases = aliases[cat]
            awards.append(awardStruct)
    return awards

awards = getAwards()
# print(awards[0].award_category.award_name)
# print(AwardNameToNominees(json.load(open('gg2013.json')), awards[0]))

data = json.load(open('gg2013.json'))
for award in awards:
    print(award.award_category.award_name)
    print(AwardNameToNominees(data, award))