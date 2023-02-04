import re
import json

#! right now I'm getting rid of 'in a' - this means that we aren't going to be able to get the completely correct award name but for right now i dont really care because it makes things easier
def standardize(text):
    ## (http[^\ ]*)|
    ## (-)|
    ## (@[^\ ]*)|
    ## |(rt\ @[^\ ]*)
    ## |(#[^\ ]*)
    text = re.sub(r'(-)|(in a)|(golden globe[^\ ]*)|(golden[^\ ]*)|(,)|(:)','',text)
    text = re.sub(r'/',' or ',text)
    text = re.sub(r'television','tv',text)
    text = re.sub(' +',' ',text).strip()
    return text

# removes all keys with a value less than min_count, then sorts the dict alphabetically if alpha = True, decreasing by value if alpha = False
def filter_and_sort_dict(dictionary,minCount=0,alpha=False):
    d = {k: v for k,v in dictionary.items() if v >= minCount}
    return dict(sorted(d.items(), key=lambda x: -x[1])) if not alpha else dict(sorted(d.items(), key=lambda x: x[0]))

# wrap text in regex
def wrap_regex(text):
    return r"(\s*" + re.escape(standardize(text)) + r".*)"

def dict_to_json(dictionary,jsonName):
    jsonob = json.dumps(dictionary, indent = 4)
    with open(f"{jsonName}.json",'w') as outfile:
        outfile.write(jsonob)

def combine_permutations(d):
    word_count = {key: len(key.split()) for key in d.keys()}
    keys = list(d.keys())
    processed_keys = set()
    result = {}
    for key in keys:
        if key in processed_keys:
            continue
        key_permutations = [(k, d[k]) for k in keys if len(k.split()) == len(key.split()) and set(k.split()) == set(key.split())]
        if len(key_permutations) > 1:
            key_permutations.sort(key=lambda x: x[0])
            primary_key = max(key_permutations, key=lambda x: len(x[0].split()))[0]
            result[primary_key] = sum([v for k, v in key_permutations])
            processed_keys.update([k for k, v in key_permutations])
        else:
            result[key] = d[key]
            processed_keys.add(key)
    return result