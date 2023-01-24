import logging


class Award:
    def __init__(self, award_category):
        self.award_category = award_category

    def __str__(self):
        return self.name

    def SetPresenters(self, presenters):
        self.presenters = presenters

    def SetWinner(self, winner):
        self.winner = winner

    def SetNominees(self, nominees):
        self.nominees = nominees

    def print_for_autograder(self):
        logging.info(self.name)
