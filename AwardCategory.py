import spacy
import re
class AwardCategory:
    def __init__(self, award_name,count=0):
        self.award_name = str(award_name)
        self.count = count
        self.aliases = set([self.award_name])
        self.isPerson = re.search(r"(actor)|(actress)|(director)|(song)",self.award_name) != None

    def __str__(self):
            return f"{self.award_name}"