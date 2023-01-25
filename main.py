from decouple import config
from Award import Award
from Mocks import Mocks
import logging
import host
import json

MOCK_AWARD_CATEGORIES = config(
    'MOCK_AWARD_CATEGORIES', cast=bool, default=False)
MOCK_AWARD_PRESENTERS = config(
    'MOCK_AWARD_PRESENTERS', cast=bool, default=False)
MOCK_AWARD_WINNERS = config('MOCK_AWARD_WINNERS', cast=bool, default=False)
MOCK_AWARD_NOMINEES = config('MOCK_AWARD_NOMINEES', cast=bool, default=False)
MOCK_HOSTS = config('MOCK_HOSTS', cast=bool, default=False)


class Main:
    def __init__(self):
        self.mocks = Mocks()
        self.tweets = json.load(open('gg2013.json'))

    def run(self):
        self.get_award_categories()
        self.get_all_award_presenters()
        self.get_award_nominees()
        self.get_award_winners()
        self.get_hosts()

    def export(self):
        # TODO - implement actual code
        for award in self.awards:
            award.print_for_autograder()

    def get_award_categories(self):
        award_categories = []
        if MOCK_AWARD_CATEGORIES:
            logging.info("Mocking award categories")
            award_categories = self.mocks.get_award_categories()
        else:
            logging.info("Not mocking award categories")
            # award_categories = self.get_award_categories()
        self.awards: list[Award] = []
        for award_category in award_categories:
            self.awards.append(Award(award_category))

    def get_all_award_presenters(self):
        for award in self.awards:
            if MOCK_AWARD_PRESENTERS:
                logging.info("Mocking award presenters")
                award.SetPresenters(
                    self.mocks.get_presenter_for_award(award))
            else:
                # print("Not mocking award presenters")
                award.SetPresenters(self.get_presenter_for_award(award))

    def get_presenter_for_award(self, award):
        # TODO - implement actual code
        return ""

    def get_award_nominees(self):
        for award in self.awards:
            if MOCK_AWARD_NOMINEES:
                logging.info("Mocking award nominees")
                award.SetNominees(
                    self.mocks.get_nominees_for_award(award))
            else:
                # print("Not mocking award nominees")
                award.SetNominees(self.get_nominees_for_award(award))

    def get_nominees_for_award(self, award):
        # TODO - implement actual code
        return []

    def get_award_winners(self):
        for award in self.awards:
            if MOCK_AWARD_WINNERS:
                logging.info("Mocking award winners")
                award.SetWinner(self.mocks.get_winner_for_award(award))
            else:
                # print("Not mocking award winners")
                award.SetWinner(self.get_winner_for_award(award))

    def get_winner_for_award(self, award):
        # TODO - implement actual code
        return ""

    def get_hosts(self):
        if MOCK_HOSTS:
            logging.info("Mocking hosts")
            self.hosts = self.mocks.get_hosts()
        else:
            logging.info("Not mocking hosts")
            # TODO - implement actual code
            self.hosts = host.find_host(self.tweets)


if __name__ == '__main__':
    main = Main()
    main.run()
    main.export()
