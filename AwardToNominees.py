import re
import spacy
import numpy as np
import Runner

def find_and_count_names(data, award_name):
    # loads name processor
    langProcesor = spacy.load("en_core_web_sm")
    nameCountArray = []
    tweetArray = []
    # Iterates through tweets
    for tweet in data:
        text = tweet['text']
        # Checks if tweet is relation to a host or hostess
        if re.search(r"\s*([Nn]ominate|[Nn]ominated|[Nn]ominee|[Nn]ominees).*award.*", text) and not text in tweetArray:
            tweetArray.append(text)
        if re.search(r"\s*award.*([[Nn]ominate|[Nn]ominated|[Nn]ominee|[Nn]ominees]).*", text) and not text in tweetArray:
            tweetArray.append(text)
    
    addNames = []
    for tweet in tweetArray:
        classifiedText = langProcesor(tweet)
        # adds name to list
        for name in classifiedText.ents:
            if name.label_ == "PERSON":
                addNames.append(name.text)
        # updates count if name exists or adds name if does not exist yet
        for name in addNames:
            exists = False
            for entries in nameCountArray:
                if entries[0] == name:
                    exists = True
                    entries[1] = entries[1] + 1
            if exists == False:
                nameCountArray.append([name, 1])
        
    return nameCountArray

def process_tweets(tweets, award_name):
    pass

def get_nominees_for_award(data, award_name):
    if award_name == "cecil b. demille award":
        return []
    print(award_name)
    print(find_and_count_names(data, award_name))
    breakpoint()
    return []

if __name__ == '__main__':
    runner = Runner.Runner()
    runner.get_award_categories("2013")
    runner.get_award_nominees("2013")
