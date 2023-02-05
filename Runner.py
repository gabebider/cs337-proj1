import argparse
import os
import sys
from decouple import config
from Award import Award
import logging
from TweetsToHost import find_host
from AwardNamesToPresenters import find_presenters
import json
# Import gg_apifake.py from the autograder directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'autograder'))
import gg_apifake
import gg_api
import autograder

# https://www.geeksforgeeks.org/singleton-method-python-design-patterns/

MOCK_AWARD_CATEGORIES = config('MOCK_AWARD_CATEGORIES', cast=bool, default=False)
MOCK_AWARD_PRESENTERS = config('MOCK_AWARD_PRESENTERS', cast=bool, default=False)
MOCK_AWARD_WINNERS = config('MOCK_AWARD_WINNERS', cast=bool, default=False)
MOCK_AWARD_NOMINEES = config('MOCK_AWARD_NOMINEES', cast=bool, default=False)
MOCK_HOSTS = config('MOCK_HOSTS', cast=bool, default=False)


class Runner:

    __shared_instance = 'runner'

    @staticmethod
    def getInstance(year=None):
        """Static Access Method"""
        if Runner.__shared_instance == 'runner':
            Runner(year)
        return Runner.__shared_instance

    def __init__(self, year):
        """virtual private constructor"""
        Runner.__shared_instance = self

        self.tweets = json.load(open(f'gg{year}.json'))

    def get_award_categories(self, year):
        award_categories = []
        if MOCK_AWARD_CATEGORIES:
            print("Mocking award categories")
            award_categories = gg_apifake.get_awards(year)
        else:
            print("Not mocking award categories")
            # award_categories = self.get_award_categories()
        self.awards: list[Award] = []
        for award_category in award_categories:
            self.awards.append(Award(award_category))

    def get_all_award_presenters(self, year):
        if MOCK_AWARD_PRESENTERS:
            print("Mocking award presenters")
            presenters = gg_apifake.get_presenters(year)
            for category in presenters.keys():
                for award in self.awards:
                    if award.award_category == category:
                        award.SetPresenters(presenters[category])
        else:
            for award in self.awards:
                award.SetPresenters(self.get_presenter_for_award(award))

    def get_presenter_for_award(self, award):
        return find_presenters(self.tweets,award)

    def get_award_nominees(self, year):
        if MOCK_AWARD_NOMINEES:
            print("Mocking award nominees")
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
        return self.awards

    def get_award_winners(self, year):
        if MOCK_AWARD_WINNERS:
            print("Mocking award winners")
            winners = gg_apifake.get_winner(year)
            for category in winners.keys():
                for award in self.awards:
                    if award.award_category == category:
                        award.SetWinner(winners[category])

        else:
            for award in self.awards:
                print("Not mocking award winners")
                award.SetWinner(self.get_winner_for_award(award))

    def get_winner_for_award(self, award):
        # TODO - implement actual code
        return ""

    def get_hosts(self, year):
        if MOCK_HOSTS:
            print("Mocking hosts")
            self.hosts = gg_apifake.get_hosts(year)
        else:
            print("Not mocking hosts")
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

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', dest='year', action='store', help='the year of the awards to get', nargs=1)
    parser.add_argument("--autograde", nargs='*', default=None, help='call the autograder which will output autograded information')
    parser.add_argument('--output_results', dest='output_results', action='store_true', help='output a human readable version of the awards that have been found')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_arguments()

    # TODO - make sure this works
    if args.year:
        year = args.year[0]
        try:
            year = int(year)
            if year < 1900 or year > 2022:
                raise ValueError("Year must be between 2013 and 2022")
        except ValueError:
            print("Invalid year: {}".format(year))
            sys.exit(1)
    else:
        year = '2013'
    runner = Runner.getInstance(year)

    autograde = False
    functions = ["hosts", "awards", "nominees", "presenters", "winner"]
    if args.autograde is not None:
        autograde = True
        if len(args.autograde) > 0:
            functions = args.autograde

    os.system('cls' if os.name == 'nt' else 'clear')
    if autograde:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Running autograder.py with the following arguments: {} {}".format(year, " ".join(functions)))
        print("Mocking the following: ")
        mocks = {
            "MOCK_AWARD_CATEGORIES": MOCK_AWARD_CATEGORIES,
            "MOCK_AWARD_NOMINEES": MOCK_AWARD_NOMINEES,
            "MOCK_AWARD_PRESENTERS": MOCK_AWARD_PRESENTERS,
            "MOCK_AWARD_WINNERS": MOCK_AWARD_WINNERS,
            "MOCK_HOSTS": MOCK_HOSTS
        }
        for key in mocks.keys():
            print("{}: {}".format(key, mocks[key]))
        print("")
        # Save it to a file
        autograder.main([year], functions)

    if args.output_results:
        if not autograde:
            runner.get_award_categories(year)
            runner.get_hosts(year)
            runner.get_all_award_presenters(year)
            runner.get_award_nominees(year)
            runner.get_award_winners(year)

            for award in runner.get_awards(year):
                print(str(award) + "\n")
        else:
            for award in gg_api.get_award_objects(year):
                print(str(award) + "\n")
