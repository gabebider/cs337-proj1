import json
import nltk
nltk.download('names')
from nltk.corpus import names
import re
from datetime import datetime
from Award import Award
from AwardCategory import AwardCategory
from collections import defaultdict
from TweetsNearMedian import TweetsNearMedian
import spacy
from utils import standardize, get_csv_set, dict_to_json, preprocess, build_iterative_regex
from TweetsByTime import Tweets_By_Time

def AwardNameToNominees(tweets, award,blacklist):
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

    male_names = names.words('male.txt')
    female_names = names.words('female.txt')

    def gender_classifier(name):
        if name.lower().capitalize() in male_names:
            return 'male'
        elif name.lower().capitalize() in female_names:
            return 'female'
        else:
            return 'unknown'

    def filter_tweets_for_good_words(tweets):
        good_words = ["nominated","nominate","nominee","robbed","stolen","rob","lost","can't believe","hope","should","did","didn't","think","would","deserved","should","better"]
        bad_words = ["present","presents","presenting"]
        for alias in award.award_category.aliases:
            good_words.append(alias)

        good_words_regex = build_iterative_regex(good_words)
        bad_words_regex = build_iterative_regex(bad_words)
        return [tweet for tweet in tweets if re.search(good_words_regex, tweet['text']) and not re.search(bad_words_regex, tweet['text'])]

    if not isinstance(award, Award):
        raise TypeError("award must be a list")


    def ultra_standardize(text):
        text = text.lower()
        text = text.replace(" has ", "")
        return text

    def combine_nominees(d,check_set):
        d = dict(sorted(d.items(), key = lambda x: -len(x[0].split())))
        new_d = defaultdict(int)
        for nom, count in d.items():
            merged = False
            for nnom in new_d:
                ## for movies, might need to check that both are in the check_set??
                if check_set != None and nnom not in check_set:
                    continue
                if nom in nnom :
                    new_d[nnom] += count
                    merged = True
                    break
            if not merged:
                new_d[nom] = count
        
        return dict(sorted(new_d.items(), key=lambda x: -x[1]))

            

    def check_for_pattern(tweet, pattern, forward: bool,filePath="test_files/nomineetweets.txt",weight=1):
        if not isinstance(forward, bool):
            raise TypeError("forward must be a boolean")
        if not isinstance(tweet, str):
            raise TypeError("tweet must be a string")
        
        tweet = tweet.lower()
        
        patternSearch = re.search(rf" {pattern} ",tweet)
        if patternSearch:
            # TODO: add try except here 
            startInd, endInd = patternSearch.span()
            if forward:
                subTweet = tweet[endInd:]
                # nominated_index = tweet.split().index(pattern.split()[-1])
            else:
                subTweet = tweet[:startInd]
            #     nominated_index = tweet.split().index(pattern.split()[0])
            # else:
            #     nominated_index = tweet.split().index(pattern)
            # f = open(filePath,"a")
            # f.write(f"\n    {tweet}")
            # f.close()

            splitSubTweet = subTweet.split()

            if forward:
                for i in range(0,len(splitSubTweet)):
                    nominee = "".join([splitSubTweet[j] + " " for j in range(i+1)])
                    nominee_candidates[nominee.strip()] += weight
            else:
                for i in range(len(splitSubTweet)-1,-1,-1):
                    nominee = "".join([splitSubTweet[j] + " " for j in range(i,len(splitSubTweet))])
                    nominee_candidates[nominee.strip()] += weight



    def check_for_people(tweet):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(ultra_standardize(tweet))
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                nominee_candidates[ent.text] += 1


    def check_for_media(tweet,media_set):
        with open("test_files/check_media.txt","a") as f:
            for media in media_set:
                if media in tweet.lower():
                    nominee_candidates[media] += 1
                    f.write(f"\n {media}")
        

    
    award_aliases = award.award_category.aliases
    relevant_tweets = TweetsNearMedian(tweets=tweets,award_name_aliases=award_aliases,min_before=2,min_After=3)
    ## attempt to filter out winner from previous award
    relevant_tweets = [tweet for tweet in relevant_tweets if "speech" not in tweet['text']]
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
    to_smush = [tweet['text'] for tweet in filter_tweets_for_good_words(tweets)]

    for tweet in tweets:
        
        # just the text please
        tweet = ultra_standardize(tweet['text'])


        weight = 2
        # check all aliases for award names
        check_for_pattern(tweet, "should win", False,weight)
        check_for_pattern(tweet, "should have gotten", False,weight)
        check_for_pattern(tweet, "should've won", False,weight)
        check_for_pattern(tweet, "better win",False,weight)
        check_for_pattern(tweet, "was robbed",False,weight)
        check_for_pattern(tweet, "didn[']?t win",False,weight)
        check_for_pattern(tweet, "was nominated",False,weight)
        check_for_pattern(tweet, "belongs to",True,weight)
        check_for_pattern(tweet, "deserves to win",False,weight)
        check_for_pattern(tweet, "was going to win",False,weight)
        check_for_pattern(tweet, "beat",False,weight)
        check_for_pattern(tweet, "beat",True,weight)
        check_for_pattern(tweet, "goes to",True,weight)
        check_for_pattern(tweet, "(wins)|(\b(?<!\shave)\bwon)",False,weight)
        check_for_pattern(tweet, "((shouldn[']?t)|(should)) have (won|been)", False,weight)



    # nominee_candidates = {k:v for k,v in nominee_candidates.items() if v>1}
    
    
    actors = get_csv_set("people.csv")
    movies = get_csv_set("movies.csv")
    series = get_csv_set("series.csv")
    # print(to_smush)

    if award.award_category.award_type == "PERSON":

        hosts = blacklist
        SUPERMEGATWEET = "".join([tweet + " " for tweet in to_smush])
        # SUPERMEGATWEET = SUPERMEGATWEET[:10000]
        check_for_people(SUPERMEGATWEET)

        nominee_candidates = {k:v for k,v in nominee_candidates.items() if k in actors and v > 1 and k not in hosts}
        nominee_candidates = combine_nominees(nominee_candidates,actors)

        if "actor" in award.award_category.award_name:
            nominee_candidates = {k:v for k,v in nominee_candidates.items() if gender_classifier(k.split()[0]) != 'female'}
        elif "actress" in award.award_category.award_name:
            nominee_candidates = {k:v for k,v in nominee_candidates.items() if gender_classifier(k.split()[0]) != 'male'}

    elif award.award_category.award_type == "MOVIE":
        
        for tweet in to_smush:
            check_for_media(tweet,movies)

        nominee_candidates = {k:v for k,v in nominee_candidates.items() if k in movies and v > 1}
        nominee_candidates = combine_nominees(nominee_candidates,movies)



    elif award.award_category.award_type == "SERIES":
        
        for tweet in to_smush:
            check_for_media(tweet,series)

        nominee_candidates = {k:v for k,v in nominee_candidates.items() if k in series and v > 1}
        nominee_candidates = combine_nominees(nominee_candidates,series)


    else:
        nominee_candidates = {k:v for k,v in nominee_candidates.items() if k not in actors and k not in movies and v > 1} 
        nominee_candidates = combine_nominees(nominee_candidates,None)

    nominee_candidates = dict(sorted(nominee_candidates.items(), key=lambda x: -x[1]))
    
    # return nominee_candidates
    
    return [nom for i,nom in enumerate(nominee_candidates.keys()) if i < 5]

def test():
    startTime = datetime.now()
    dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
    print("[TEST] process started at =", dt_string)

    with open("award_aliases.json", "r") as file:
        awards = json.load(file)

    tweets = preprocess(json.load(open(f'gg2013.json')))

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
        nom_candidates = AwardNameToNominees(tweets, aw,{'amy poehler','tina fey'})

        aaaa[aw.award_category.award_name] = nom_candidates
    
    dict_to_json(aaaa,"nominees",False,"test_files/")  

    endTime = datetime.now()
    dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
    print("[TEST] process ended at =", dt_string)
    print("[TEST] duration:",str(endTime-startTime))


if __name__ == "__main__":
    test()  
  