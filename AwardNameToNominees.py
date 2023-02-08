import json
import re
from datetime import datetime
from Award import Award
from AwardCategory import AwardCategory
from collections import defaultdict
from EliWhat import EliWhat
import spacy
from utils import standardize, get_csv_set, dict_to_json, preprocess
from TweetsByTime import Tweets_By_Time

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
        text = text.lower()
        text = text.replace(" has ", "")
        return text

    def check_for_pattern(tweet, pattern, forward: bool,filePath="test_files/nomineetweets.txt"):
        if not isinstance(forward, bool):
            raise TypeError("forward must be a boolean")
        if not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        
        f = open(filePath,"a")
        tweet = tweet.lower()
        f.write(f"\n{pattern}\n")
        f.close()
        
        patternSearch = re.search(rf" {pattern} ",tweet)
        if patternSearch:
            # TODO: add try except here 
            startInd, endInd = patternSearch.span()
            if forward:
                subTweet = tweet[endInd+1:]
                # nominated_index = tweet.split().index(pattern.split()[-1])
            else:
                subTweet = tweet[:startInd]
            #     nominated_index = tweet.split().index(pattern.split()[0])
            # else:
            #     nominated_index = tweet.split().index(pattern)
            f = open(filePath,"a")
            f.write(f"\n    {tweet}")
            f.close()

            splitSubTweet = subTweet.split()

            if forward:
                for i in range(0,len(splitSubTweet)):
                    nominee = "".join([splitSubTweet[j] + " " for j in range(i+1)])
                    nominee_candidates[nominee.strip()] += 1
            else:
                for i in range(len(splitSubTweet)-1,-1,-1):
                    nominee = "".join([splitSubTweet[j] + " " for j in range(i,len(splitSubTweet))])
                    nominee_candidates[nominee.strip()] += 1



            # if forward:
            #     for i in range(nominated_index + 1, len(tweet.split())):
            #         nominee = ""
            #         for j in range(nominated_index + 1, i + 1):
            #             nominee += tweet.split()[j] + " "
            #         nominee = nominee.strip()
            #         nominee_candidates[nominee] += 1
            # else:
            #     for i in range(nominated_index - 1, -1, -1):
            #         nominee = ""
            #         for j in range(i, nominated_index):
            #             nominee += tweet.split()[j] + " "
            #         nominee = nominee.strip()
            #         nominee_candidates[nominee] += 1


    def check_for_people(tweet):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(ultra_standardize(tweet))
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                nominee_candidates[ent.text] += 1

    
    award_aliases = award.award_category.aliases
    relevant_tweets = EliWhat(tweets=tweets,award_name_aliases=award_aliases,minBefore=3,minAfter=1.5)
    # remove all duplicate tweets
    unique_tweets = []
    unique_text = set()

    #! change this stuff eventually
    for tweet in relevant_tweets:
        text = tweet['text']
        if text not in unique_text:
            unique_text.add(text)
            unique_tweets.append(tweet)
    # now we have a set of unique tweets to work with
    tweets = unique_tweets

    nominee_candidates = defaultdict(int)
    # tracker = 0
    # loop through all tweets
    for tweet in tweets:
        
        # just the text please
        tweet = ultra_standardize(tweet['text'])
        # check all aliases for award names
        check_for_pattern(tweet, "should win", False)
        check_for_pattern(tweet, "should have gotten", False)
        check_for_pattern(tweet, "should've won", False)
        check_for_pattern(tweet, "better win",False)
        check_for_pattern(tweet, "was robbed",False)
        check_for_pattern(tweet, "didn[']?t win",False)
        check_for_pattern(tweet, "was nominated",False)
        check_for_pattern(tweet, "belongs to",True)
        check_for_pattern(tweet, "deserves to win",False)
        check_for_pattern(tweet, "was going to win",False)
        check_for_pattern(tweet, "beat",False)
        check_for_pattern(tweet, "beat",True)
        check_for_pattern(tweet, "goes to",True)
        check_for_pattern(tweet, "(wins)|(\bwon\b(?!\shave))",False)
        check_for_pattern(tweet, "((shouldn[']?t)|(should)) have (won|been)", False)

    # nominee_candidates = {k:v for k,v in nominee_candidates.items() if v>1}
    nominee_candidates = dict(sorted(nominee_candidates.items(), key=lambda x: -x[1]))
    
    actors = get_csv_set("people.csv")
    movies = get_csv_set("movies.csv")

    if award.award_category.award_type == "PERSON":
        nominee_candidates = {k:v for k,v in nominee_candidates.items() if k in actors and v > 1}
    elif award.award_category.award_type == "MOVIE":
        nominee_candidates = {k:v for k,v in nominee_candidates.items() if k in movies and v > 1}
    else:
        nominee_candidates = {k:v for k,v in nominee_candidates.items() if k not in actors and k not in movies and v > 1} 
    
    # return nominee_candidates
    
    return [nom for i,nom in enumerate(nominee_candidates.keys()) if i < 5]

def test():
    startTime = datetime.now()
    dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
    print("[TEST] process started at =", dt_string)

    with open("award_aliases.json", "r") as file:
        awards = json.load(file)

    tweets = json.load(open(f'gg2013.json'))

    aaaa = dict()
    i = 0
    for key,award in awards.items():
        print(key)
        awc = AwardCategory(key)
        awc.aliases = award[1]
        awc.count = award[0]
        aw = Award(awc)
        i += 1

        with open("test_files/nomineetweets.txt","a") as f:
            f.write(f"\n\n\n[{key}]")
        nom_candidates = AwardNameToNominees(tweets, aw)

        aaaa[aw.award_category.award_name] = nom_candidates
    
    dict_to_json(aaaa,"nominees",False,"test_files/")  

    endTime = datetime.now()
    dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
    print("[TEST] process ended at =", dt_string)
    print("[TEST] duration:",str(endTime-startTime))


if __name__ == "__main__":
    test()  
  