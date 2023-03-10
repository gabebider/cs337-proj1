import re
import json
from unidecode import unidecode
import csv
from datetime import datetime

def preprocess(tweets):

    for i,tweet in enumerate(tweets):
        # print(tweet['text'])
        # print(standardize(tweet['text']))
        tweets[i]['text'] = standardize(tweet['text'])
    return tweets

def standardize(text):
    ## (http[^\ ]*)|
    ## (-)|
    ## (@[^\ ]*)|
    ## |(rt\ @[^\ ]*)
    ## |(#[^\ ]*)
    ## (-)|
    # text = unidecode(text)
    text = text.replace("@", "")
    text = text.replace("\"", "")
    text = text.replace("&amp","")
    # bad_words = {'a','our','your','their','an','i' ,'you','we','us','her', 'and', 'are', 'as', 'at', 'be', 'by', 'from', 'has', 'he', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'with'}
    punctuation = {':',"#",',','-','.','!','?'}
    for p in punctuation:
        text = text.replace(p,"")
    # for bad_word in bad_words:
    #     # print(text)
    #     text = text.replace(f" {bad_word} ","  ")
        # print(text)
    text = text.replace("'"," ")
    text = re.sub(r'(?i)(golden globe[^\ ]*)|(golden[^\ ]*)','',text)
    text = re.sub(r"(?i)television","tv",text)
    text = re.sub(r"(?i)mini ","mini",text)
    ## i struggle with regex
    text = re.sub(r"(?i) series"," tv series",text)
    text = re.sub(r"(?i)tv tv","tv",text)
    text = re.sub(r"(?i) tv ", " tv series ", text)
    text = re.sub(r"(?i)tv series series", "tv series", text)
    text = re.sub(r"(?i)tv series movie", "tv movie", text)

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
    regexes.append(r'(?i)')
    for alias in aliases:
        regexes.append(wrap_regex(alias))
        regexes.append(r"|")
    regexes.pop()
    return ''.join(regexes)

def get_csv_set(csv_file):
    csvSet = set()
    with open(csv_file, 'r', encoding='utf-8') as file:
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
    