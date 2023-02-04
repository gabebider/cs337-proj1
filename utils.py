import re
import json

#! right now I'm getting rid of 'in a' - this means that we aren't going to be able to get the completely correct award name but for right now i dont really care because it makes things easier
def standardize(text):
    ## (http[^\ ]*)|
    ## (-)|
    ## (@[^\ ]*)|
    ## |(rt\ @[^\ ]*)
    ## |(#[^\ ]*)
    text = re.sub(r'(-[\ ]*)|(in\ a[\ ]*)|(golden globe[^\ ]*[\ ]*)|(golden[^\ ]*[\ ]*)|(,)|(:)','',text)
    text = re.sub(r'/',' or ',text)
    text = re.sub(r'television','tv',text)
    return text

# removes all keys with a value less than min_count, then sorts the dict in decreasing order by value
def filter_and_sort_dict(dictionary,minCount=0):
    d = {k: v for k,v in dictionary.items() if v >= minCount}
    return dict(sorted(d.items(), key=lambda x: -x[1]))

# wrap text in regex
def wrap_regex(text):
    return r"(\s*" + re.escape(standardize(text)) + r".*)"

def dict_to_json(dictionary,jsonName):
    jsonob = json.dumps(dictionary, indent = 4)
    with open(f"{jsonName}.json",'w') as outfile:
        outfile.write(jsonob)