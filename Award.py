import logging


class Award:
    def __init__(self, award_category):
        self.award_category = award_category
        self.presenters = []
        self.winner = ""
        self.nominees = []

    def __str__(self):
        return f"Award: {self.award_category}\n Presenters: {self.presenters}\n Nominees: {self.nominees}\n Winner: {self.winner}"

    def SetPresenters(self, presenters):
        self.presenters = presenters

    def SetWinner(self, winner):
        self.winner = winner

    def SetNominees(self, nominees):
        self.nominees = nominees

    def print_for_autograder(self):
        logging.info(self.name)
