import json
import re

data = json.load(open('gg2013.json'))

djangoCount = 0
argoCount = 0

for item in data:
    text = item['text'].lower()

    if re.match(r".*django unchained.*", text):
        # print(item['text'])
        djangoCount += 1
    
    if re.match(r".*argo.*", text):
        # print(item['text'])
        argoCount += 1

print(f"djangoCount: {djangoCount}")
print(f"argoCount: {argoCount}")
