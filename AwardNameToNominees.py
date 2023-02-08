import json
import re
from Award import Award
from AwardCategory import AwardCategory
from collections import defaultdict
import spacy
from utils import standardize, get_csv_set, dict_to_json
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

    def check_for_pattern(tweet, award, pattern, forward: bool):
        if not isinstance(forward, bool):
            raise TypeError("forward must be a boolean")
        if not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        if not isinstance(award, Award):
            raise TypeError("award must be an Award object")
        
        if re.search( rf" {pattern} ", tweet):
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
                    nominee_candidates[nominee] += 1
            else:
                for i in range(nominated_index - 1, -1, -1):
                    nominee = ""
                    for j in range(i, nominated_index):
                        nominee += tweet.split()[j] + " "
                    nominee = nominee.strip()
                    nominee_candidates[nominee] += 1

    def check_for_people(tweet):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(ultra_standardize(tweet))
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                nominee_candidates[ent.text] += 1

    
    award_aliases = award.award_category.aliases
    relevant_tweets = Tweets_By_Time(tweets=tweets,award_name_aliases=award_aliases,range=0.3)
    # remove all duplicate tweets
    unique_tweets = []
    unique_text = set()
    for tweet in relevant_tweets:
        text = tweet['text'].lower()
        if text not in unique_text:
            unique_text.add(text)
            unique_tweets.append(tweet)
    # now we have a set of unique tweets to work with
    tweets = unique_tweets

    nominee_candidates = defaultdict(int)
    tracker = 0
     # loop through all tweets
    for tweet in tweets:
        if tracker % 5000 == 0:
            print(f"Looking at tweet {tracker} of {len(tweets)}")
        tracker += 1
        
        # just the text please
        tweet = ultra_standardize(tweet['text'])
        # check all aliases for award names
        check_for_pattern(tweet, award, "should win", False)
        check_for_pattern(tweet, award, "should have won", False)
        check_for_pattern(tweet, award, "shouldn't have won", False)
        check_for_pattern(tweet, award, "should have been", False)
        check_for_pattern(tweet, award, "shouldn't have been", False)
        check_for_pattern(tweet, award, "should have gotten", False)

    # please don't judge me for this
    if award.award_category.award_type == "PERSON":
        SUPERMEGATWEET = ''.join(tweet["text"] + " " for tweet in tweets[:3000])
        check_for_people(SUPERMEGATWEET)

    nominee_candidates = {k:v for k,v in nominee_candidates.items() if v>1}
    nominee_candidates = dict(sorted(nominee_candidates.items(), key=lambda x: -x[1]))
    
    actors = get_csv_set("people.csv")
    movies = get_csv_set("movies.csv")

    if award.award_category.award_type == "PERSON":
        nominee_candidates = {k:v for k,v in nominee_candidates.items() if k in actors}
    else:
        nominee_candidates = {k:v for k,v in nominee_candidates.items() if k in movies}
    
    return [nom for i,nom in enumerate(nominee_candidates.keys()) if i < 5]

def test():
    with open("award_aliases.json", "r") as file:
        awards = json.load(file)

    tweets = json.load(open(f'gg2013.json'))

    actors = get_csv_set("people.csv")
    movies = get_csv_set("movies.csv")

    aaaa = dict()
    i = 0
    for key,award in awards.items():
        awc = AwardCategory(key)
        awc.aliases = award[1]
        awc.count = award[0]
        aw = Award(awc)
        i += 1

        nom_candidates = AwardNameToNominees(tweets, aw)
        nom_candidates = {k:v for k,v in nom_candidates.items() if v>1}
        nom_candidates = dict(sorted(nom_candidates.items(), key=lambda x: -x[1]))
        
        if awc.isPerson:
            nom_candidates = {k:v for k,v in nom_candidates.items() if k in actors}
        else:
            nom_candidates = {k:v for k,v in nom_candidates.items() if k in movies}

        aaaa[aw.award_category.award_name] = nom_candidates
    
    dict_to_json(aaaa,"aaaa",False,"test_files/")    
  