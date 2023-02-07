import re
import json
import csv
from datetime import datetime

def preprocess(tweets):
    ## get rid of all retweets
    tweets = {tweet for tweet in tweets if tweet['text'][0:2] != "RT"}
    for tweet in tweets:
        tweet['text'] = standardize(tweet['text'])
    return tweets

#! right now I'm getting rid of 'in a' - this means that we aren't going to be able to get the completely correct award name but for right now i dont really care because it makes things easier
def standardize(text):
    ## (http[^\ ]*)|
    ## (-)|
    ## (@[^\ ]*)|
    ## |(rt\ @[^\ ]*)
    ## |(#[^\ ]*)
    ## (-)|
    text = re.sub(r'(golden globe[^\ ]*)|(golden[^\ ]*)|(:)|(#)','',text)
    text = text.replace("television","tv")
    text = text.replace("tv series","series")
    text = text.replace("mini ","mini")
    text = text.replace("/"," or ")
    text = re.sub(' +',' ',text).strip()
    return text

# removes all keys with a value less than min_count, then sorts the dict alphabetically if alpha = True, decreasing by value if alpha = False
def filter_dict(d,minCount=0):
    return {k: v for k,v in d.items() if v >= minCount}

def sort_dict_decreasing_count(d):
    return dict(sorted(d.items(), key=lambda x: -x.count))

def sort_dict_alpha(d):
    return dict(sorted(d.items(), key=lambda x: x[0]))
# wrap text in regex
def wrap_regex(text):
    return r"(\s*" + re.escape(standardize(text)) + r".*)"

def dict_to_json(dictionary,jsonName,award=False,folderName="test_files/"):
    if award:
        dictionary = {k: (v.count, list(v.aliases)) for k,v in dictionary.items()}
    jsonob = json.dumps(dictionary, indent = 4)
    with open(f"{folderName}{jsonName}.json",'w') as outfile:
        outfile.write(jsonob)

def build_iterative_regex(aliases):
    regexes = []
    for alias in aliases:
        regexes.append(wrap_regex(alias))
        regexes.append(r"|")
    regexes.pop()
    return ''.join(regexes)

def get_csv_set(csv_file):
    csvSet = set()
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for name in row:
                csvSet.add(name.lower())
    return csvSet

## just an example for copypasting
def example_time():
    startTime = datetime.now()
    dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
    print("[FILL IN] process started at =", dt_string)


    endTime = datetime.now()
    dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
    print("[FILL IN] process ended at =", dt_string)
    print("[FILL IN] duration:",str(endTime-startTime))
    