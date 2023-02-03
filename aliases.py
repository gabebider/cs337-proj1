import json
import re

award_aliases = {
    'best motion picture - drama': [
        'best motion picture - drama',
        'best picture drama',
        'best drama',
    ],
    'best performance by an actress in a motion picture - drama': [
        'best performance by an actress in a motion picture - drama',
        'best actress drama',
        'best actress motion picture',
        'best actress motion picture drama',
    ],
    'best performance by an actor in a motion picture - drama': [
        'best performance by an actor in a motion picture - drama',
        'best actor drama',
        'best actor motion picture',
        'best actor motion picture drama',
    ],
    'best motion picture - comedy or musical': [
        'best motion picture - comedy or musical',
        'best picture comedy or musical',
        'best comedy or musical',
    ],
    'best performance by an actress in a motion picture - comedy or musical': [
        'best performance by an actress in a motion picture - comedy or musical',
        'best actress motion picture comedy or musical',
        'best actress comedy or musical',
        'best actress in a comedy or musical',
        'best actress in a motion picture - comedy or musical'
    ],
    'best performance by an actor in a motion picture - comedy or musical': [
        'best performance by an actor in a motion picture - comedy or musical',
        'best actor motion picture comedy or musical',
        'best actor in a motion picture - comedy or musical',
        'best actor comedy or musical',
        'best actor in a comedy or musical',
    ],
    'best animated feature film': [
        'best animated feature film',
        'best animated film',
        'best animated',
    ],
    'best foreign language film': [
        'best foreign language film',
        'best foreign film',
        'best foreign',
    ],
    'best performance by an actress in a supporting role in a motion picture': [
        'best performance by an actress in a supporting role in a motion picture',
        'best actress in a supporting role in a motion picture',
        'best supporting actress in a motion picture',
        'best supporting actress motion picture',        
    ],
    'best performance by an actor in a supporting role in a motion picture': [
        'best performance by an actor in a supporting role in a motion picture',
        'best supporting actor in a motion picture',
        'best supporting actor motion picture',
    ],
    'best director - motion picture': [
        'best director - motion picture',
        'best director in a motion picture',
        'best director for a motion picture',
        'best director',
    ],
    'best screenplay - motion picture': [
        'best screenplay - motion picture',
        'best screenplay in a motion picture',
        'best screenplay for a motion picture',
        'best screenplay',
    ],
    'best original score - motion picture': [
        'best original score - motion picture',
        'best original score in a motion picture',
        'best score',
        'best original score',
    ],
    'best original song - motion picture': [
        'best original song - motion picture',
        'best original song',
        'best song',
    ],
    'best television series - drama': [
        'best television series - drama',
        'best television drama',
    ],
    'best performance by an actress in a television series - drama': [
        'best performance by an actress in a television series - drama',
        'best actress in a television series drama',
        'best actress in a television drama',
        'best actress television series drama',
        'best actress television drama',
    ],
    'best performance by an actor in a television series - drama': [
        'best performance by an actor in a television series - drama',
        'best actor in a television drama',
        'best actor in a television series drama'
        'best actor television series drama',
        'best actor television drama',
    ],
    'best television series - comedy or musical': [
        'best television series - comedy or musical',
        'best television comedy or musical',
    ],
    'best performance by an actress in a television series - comedy or musical': [
        'best performance by an actress in a television series - comedy or musical',
        'best actress in a television series comedy or musical',
        'best actress in a television comedy or musical',
    ],
    'best performance by an actor in a television series - comedy or musical': [
        'best performance by an actor in a television series - comedy or musical',
        'best actor in a television comedy or musical',
        'best actor television comedy or musical',
        'best actor in a television series - comedy or musical',
    ],
    'best mini-series or motion picture made for television': [
        'best mini-series or motion picture made for television',
        'best television mini-series',
    ],
    'best performance by an actress in a mini-series or motion picture made for television': [
        'best performance by an actress in a mini-series or motion picture made for television',
        'best actress in a mini-series or motion picture made for television',
        'best actress in a television miniseries or motion picture',
        'best actress in a television miniseries',
    ],
    'best performance by an actor in a mini-series or motion picture made for television': [
        'best performance by an actor in a mini-series or motion picture made for television',
        'best actor in a mini-series or motion picture made for television',
        'best actor television miniseries',
        'best actor in a television miniseries',
    ],
    'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': [
        'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
        'best supporting actress in a series, mini-series or motion picture made for television',
        'best supporting actress in a television series, mini-series or motion picture',
        'best supporting actress in television',
        'best supporting actress television',
        'best television supporting actress',    
    ],
    'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': [
        'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television',
        'best supporting actor in a series, mini-series or motion picture made for television',
        'best supporting actor television',
    ]
}
'''
removes small distincitions like '-', '/' vs 'or', and 'television' vs 'tv'
removes links and retweet indicators, hashtags
'''
def standardize(text):
    text = re.sub(r'(- )|(-)|(http[^\ ]*)|(rt[\ ]*)|(#[^\ ]*)|(@[^\ ]*)','',text)
    text = re.sub(r'/',' or ',text)
    text = re.sub(r'television','tv',text)
    return text

def counts_to_json(award_aliases):
    tweets = json.load(open('gg2013.json'))


    for award in award_aliases:
        print(f"STARTING AWARD!!!!!: {award}\n")
        aliases = award_aliases[award]
        for ind,alias in enumerate(aliases):
            seenTweets = set()
            count = 0
            cleaned_alias = standardize(alias)
            for tweet in tweets:
                text = standardize(tweet['text'].lower())
                award_regex = r"\s*" + re.escape(cleaned_alias) + r".*"
                if re.search(award_regex,text) and text not in seenTweets:
                    seenTweets.add(text)
                    count += 1
            aliases[ind] = {alias: count}
    jsonob = json.dumps(award_aliases, indent = 4)
    with open("aliases.json",'w') as outfile:
        outfile.write(jsonob)


def counts_to_json_nom(award_aliases):
    tweets = json.load(open('gg2013.json'))


    for award in award_aliases:
        print(f"STARTING AWARD!!!!!: {award}\n")
        aliases = award_aliases[award]
        for ind,alias in enumerate(aliases):
            seenTweets = set()
            count = 0
            cleaned_alias = standardize(alias)
            for tweet in tweets:
                text = standardize(tweet['text'].lower())
                award_regex = r"\s*" + re.escape(cleaned_alias) + r".*"
                if re.search(award_regex,text) and text not in seenTweets and re.search(r"\s*([[Nn]ominate|[Nn]ominated|[Nn]ominee|[Nn]ominees]).*", text):
                    seenTweets.add(text)
                    count += 1
            if count > 0:
                aliases[ind] = {alias: count}
    jsonob = json.dumps(award_aliases, indent = 4)
    with open("aliases_nominees.json",'w') as outfile:
        outfile.write(jsonob)

def counts_to_json_pres(award_aliases):
    tweets = json.load(open('gg2013.json'))


    for award in award_aliases:
        print(f"STARTING AWARD!!!!!: {award}\n")
        aliases = award_aliases[award]
        for ind,alias in enumerate(aliases):
            seenTweets = set()
            count = 0
            cleaned_alias = standardize(alias)
            for tweet in tweets:
                text = standardize(tweet['text'].lower())
                award_regex = r"\s*" + re.escape(cleaned_alias) + r".*"
                if re.search(award_regex,text) and text not in seenTweets and re.search(r"\s*[Pp]resent.*", text):
                    seenTweets.add(text)
                    count += 1
            if count > 0:
                aliases[ind] = {alias: count}
    jsonob = json.dumps(award_aliases, indent = 4)
    with open("aliases_presenters.json",'w') as outfile:
        outfile.write(jsonob)

# counts_to_json(award_aliases=award_aliases)
# counts_to_json_nom(award_aliases=award_aliases)
# counts_to_json_pres(award_aliases=award_aliases)


        

