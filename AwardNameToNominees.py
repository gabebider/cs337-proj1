import json
import re
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

    with open("test_files/nomineetweets.txt","a") as f:

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
            tweet = tweet.lower()
            
            if re.search( rf" {pattern} ", tweet):
                # TODO: add try except here 
                if len(pattern.split()) > 1 and forward:
                    nominated_index = tweet.lower().split().index(pattern.split()[-1])
                elif len(pattern.split()) > 1 and not forward:
                    nominated_index = tweet.lower().split().index(pattern.split()[0])
                else:
                    nominated_index = tweet.lower().split().index(pattern)

                f.write(f"\n{tweet}")
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
            check_for_pattern(tweet, award, "should win", False)
            check_for_pattern(tweet, award, "should have won", False)
            check_for_pattern(tweet, award, "shouldn't have won", False)
            check_for_pattern(tweet, award, "should have been", False)
            check_for_pattern(tweet, award, "shouldn't have been", False)
            check_for_pattern(tweet, award, "should have gotten", False)
            check_for_pattern(tweet, award, "should've won", False)
            check_for_pattern(tweet, award, "better win",False)
            check_for_pattern(tweet, award, "was robbed",False)
            check_for_pattern(tweet, award, "didn't win",False)
            check_for_pattern(tweet, award, "didnt win",False)
            check_for_pattern(tweet, award, "was nominated",False)
            check_for_pattern(tweet, award, "belongs to",True)
            check_for_pattern(tweet, award, "deserves to win",False)
            check_for_pattern(tweet, award, "was going to win",False)
            check_for_pattern(tweet, award, "beat",False)
            check_for_pattern(tweet, award, "beat",True)

        # nominee_candidates = {k:v for k,v in nominee_candidates.items() if v>1}
        nominee_candidates = dict(sorted(nominee_candidates.items(), key=lambda x: -x[1]))
        
        actors = get_csv_set("people.csv")
        movies = get_csv_set("movies.csv")

        if award.award_category.award_type == "PERSON":
            nominee_candidates = {k:v for k,v in nominee_candidates.items() if k in actors}
        elif award.award_category.award_type == "MOVIE":
            nominee_candidates = {k:v for k,v in nominee_candidates.items() if k in movies}
        else:
            nominee_candidates = {k:v for k,v in nominee_candidates.items() if k not in actors and k not in movies}
        
        return [nom for i,nom in enumerate(nominee_candidates.keys()) if i < 4 and nominee_candidates[nom] > 1]

def test():
    with open("award_aliases.json", "r") as file:
        awards = json.load(file)

    tweets = json.load(open(f'gg2013.json'))

    actors = get_csv_set("people.csv")
    movies = get_csv_set("movies.csv")

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
        # nom_candidates = {k:v for k,v in nom_candidates.items() if v>1}
        # nom_candidates = dict(sorted(nom_candidates.items(), key=lambda x: -x[1]))
        
        # if awc.isPerson:
        #     nom_candidates = {k:v for k,v in nom_candidates.items() if k in actors}
        # else:
        #     nom_candidates = {k:v for k,v in nom_candidates.items() if k in movies}

        aaaa[aw.award_category.award_name] = nom_candidates
    
    dict_to_json(aaaa,"aaaa",False,"test_files/")  

if __name__ == "__main__":
    test()  
  