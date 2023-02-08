import spacy
import re
class AwardCategory:
    def __init__(self, award_name,count=0):
        self.award_name = str(award_name)
        self.count = count
        self.aliases = set([self.award_name])
        self.set_type()

    def __str__(self):
            return f"{self.award_name}"
    
    def set_type(self):
        peopleTypes = ["actor","actress","director"]
        otherTypes = ["song"]
        if any([kw in self.award_name for kw in peopleTypes]):
            self.award_type = "PERSON"
        elif any([kw in self.award_name for kw in otherTypes]):
            self.award_type = "OTHER"
        else:
            self.award_type = "MOVIE"