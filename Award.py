import logging
from AwardCategory import AwardCategory

class Award:
    def __init__(self, award_category:AwardCategory):
        self.award_category = award_category
        self.presenters = []
        self.winner = ""
        self.nominees = []

    def __str__(self):
        return f"Award: {self.award_category.award_name}\n Presenters: {self.presenters}\n Nominees: {self.nominees}\n Winner: {self.winner}"

    def SetPresenters(self, presenters):
        self.presenters = presenters

    def SetWinner(self, winner):
        self.winner = winner

    def SetNominees(self, nominees):
        self.nominees = nominees

    def print_for_autograder(self):
        logging.info(self.name)

    def __str__(self):
        result = f"Award Name: {self.award_category}"
        if self.presenters:
            result += f"\nPresenters: {self.presenters}"
        if self.nominees:
            result += f"\nNominees:"
            for nominee in self.nominees:
                result += f"\n\t{nominee}"
        if self.winner:
            result += f"\nWinner: {self.winner}"
        return result
