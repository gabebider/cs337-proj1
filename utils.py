import re
import json

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

def dict_to_json(dictionary,jsonName,award=False):
    if award:
        dictionary = {k: (v.count, list(v.aliases)) for k,v in dictionary.items()}
    jsonob = json.dumps(dictionary, indent = 4)
    with open(f"test_files/{jsonName}.json",'w') as outfile:
        outfile.write(jsonob)
