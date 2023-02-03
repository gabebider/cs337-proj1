from decouple import config
from Award import Award
import logging
from host import find_host
from AwardCategoriesToPresenters import find_presenters
import json
from autograder import gg_apifake

# https://www.geeksforgeeks.org/singleton-method-python-design-patterns/

MOCK_AWARD_CATEGORIES = config(
    'MOCK_AWARD_CATEGORIES', cast=bool, default=False)
MOCK_AWARD_PRESENTERS = config(
    'MOCK_AWARD_PRESENTERS', cast=bool, default=False)
MOCK_AWARD_WINNERS = config('MOCK_AWARD_WINNERS', cast=bool, default=False)
MOCK_AWARD_NOMINEES = config('MOCK_AWARD_NOMINEES', cast=bool, default=False)
MOCK_HOSTS = config('MOCK_HOSTS', cast=bool, default=False)


class Runner:

    __shared_instance = 'runner'

    @staticmethod
    def getInstance():
        """Static Access Method"""
        if Runner.__shared_instance == 'runner':
            Runner()
        return Runner.__shared_instance

    def __init__(self):
        """virtual private constructor"""
        Runner.__shared_instance = self
        self.tweets = json.load(open('gg2013.json'))

    def get_award_categories(self, year):
        award_categories = []
        if MOCK_AWARD_CATEGORIES:
            logging.info("Mocking award categories")
            award_categories = gg_apifake.get_awards(year)
        else:
            logging.info("Not mocking award categories")
            # award_categories = self.get_award_categories()
        self.awards: list[Award] = []
        for award_category in award_categories:
            self.awards.append(Award(award_category))

    def get_all_award_presenters(self, year):
        if MOCK_AWARD_PRESENTERS:
            logging.info("Mocking award presenters")
            presenters = gg_apifake.get_presenters(year)
            for category in presenters.keys():
                for award in self.awards:
                    if award.award_category == category:
                        award.SetPresenters(presenters[category])
        else:
            for award in self.awards:
                # print(award)
                # print("Not mocking award presenters")
                award.SetPresenters(self.get_presenter_for_award(award))

    def get_presenter_for_award(self, award):
        return find_presenters(self.tweets,award)

    def get_award_nominees(self, year):
        if MOCK_AWARD_NOMINEES:
            logging.info("Mocking award nominees")
            nominees = gg_apifake.get_nominees(year)
            for category in nominees.keys():
                for award in self.awards:
                    if award.award_category == category:
                        award.SetNominees(nominees[category])
        else:
            for award in self.awards:
                print("Not mocking award nominees")
                award.SetNominees(self.get_nominees_for_award(award))

    def get_nominees_for_award(self, award):
        # TODO - implement actual code
        return []

    def get_awards(self, year):
        pass

    def get_award_winners(self, year):
        if MOCK_AWARD_WINNERS:
            logging.info("Mocking award winners")
            winners = gg_apifake.get_winner(year)
            for category in winners.keys():
                for award in self.awards:
                    if award.award_category == category:
                        award.SetWinner(winners[category])

        else:
            for award in self.awards:
                logging.info("Not mocking award winners")
                award.SetWinner(self.get_winner_for_award(award))

    def get_winner_for_award(self, award):
        # TODO - implement actual code
        return ""

    def get_hosts(self, year):
        if MOCK_HOSTS:
            logging.info("Mocking hosts")
            self.hosts = gg_apifake.get_hosts(year)
        else:
            logging.info("Not mocking hosts")
            # TODO - implement actual code
            self.hosts = find_host(self.tweets)

    def export_hosts(self):
        return self.hosts

    def export_presenters(self):
        presenters = {}
        for award in self.awards:
            presenters[award.award_category] = award.presenters
        return presenters

    def export_nominees(self):
        nominees = {}
        for award in self.awards:
            nominees[award.award_category] = award.nominees
        return nominees

    def export_winners(self):
        winners = {}
        for award in self.awards:
            winners[award.award_category] = award.winner
        return winners

    def export_award_categories(self):
        awards = {}
        for award in self.awards:
            awards[award.award_category] = award
        return awards


if __name__ == '__main__':
    main = Runner()
    main.get_hosts('2013')
    main.get_award_categories('2013')
    main.get_all_award_presenters('2013')
    print(main.hosts)
    for award in main.awards:
        print(award)
    

