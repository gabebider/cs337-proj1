class Award():
    def __init__(self, award_name, nominees, presenters, winner):
        self.award_name = award_name
        self.nominees = nominees
        self.presenters = presenters
        self.winner = winner

    def __str__(self):
        return self.name

    def print_for_autograder(self):
        print(self.name, self.description, self.image)
