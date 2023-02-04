import spacy

class AwardCategory:
    def __init__(self, award_name,count=0):
        self.award_name = award_name
        self.count = count
        self.aliases = []
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.award_name)
        self.name_pos = {}
        for token in doc:
            self.name_pos[token.text] = token.pos_

