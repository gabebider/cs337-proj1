import argparse
import os
import sys
from decouple import config
from Award import Award
from datetime import datetime
from AwardCategory import AwardCategory
from AwardNameToNominees import AwardNameToNominees
from TweetsToHost import find_host
from AwardNameToPresenters import find_presenters
from TweetsToAwardNames import get_award_categories_from_json
from AwardNameToWinners import AwardNameToWinners
import json
from TweetsToRedCarpet import find_redcarpet
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
        startTime = datetime.now()
        dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
        print("[Get Award Categories] process started at =", dt_string)

        award_categories = []
        if MOCK_AWARD_CATEGORIES:
            print("Mocking award categories")
            award_categories = gg_apifake.get_awards(year)
            award_categories = [AwardCategory(category) for category in award_categories]
        else:
            print("Not mocking award categories")
            award_categories = [v for k,v in get_award_categories_from_json(self.tweets).items()]
            # award_categories = self.get_award_categories()
        self.awards: list[Award] = []
        for award_category in award_categories:
            self.awards.append(Award(award_category))

        endTime = datetime.now()
        dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
        print("[Get Award Categories] process ended at =", dt_string)
        print("[Get Award Categories] duration:",str(endTime-startTime))
 

    def get_all_award_presenters(self, year):
        startTime = datetime.now()
        dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
        print("[Get Award Presenters] process started at =", dt_string)

        if MOCK_AWARD_PRESENTERS:
            print("Mocking award presenters")
            presenters = gg_apifake.get_presenters(year)
            for category in presenters.keys():
                for award in self.awards:
                    if award.award_category.award_name == category:
                        award.SetPresenters(presenters[category])
        else:
            print("Not mocking award presenters")
            for award in self.awards:
                award.SetPresenters(self.get_presenter_for_award(award))

        endTime = datetime.now()
        dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
        print("[Get Award Presenters] process ended at =", dt_string)
        print("[Get Award Presenters] duration:",str(endTime-startTime))
        

    def get_presenter_for_award(self, award):
        return find_presenters(self.tweets,award)

    def get_award_nominees(self, year):
        startTime = datetime.now()
        dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
        print("[Get Award Nominees] process started at =", dt_string)

        if MOCK_AWARD_NOMINEES:
            print("Mocking award nominees")
            nominees = gg_apifake.get_nominees(year)
            for category in nominees.keys():
                for award in self.awards:
                    if award.award_category.award_name == category:
                        award.SetNominees(nominees[category])
        else:
            print("Not mocking award nominees")
            for award in self.awards:
                award.SetNominees(self.get_nominees_for_award(award))

        endTime = datetime.now()
        dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
        print("[Get Award Nominees] process ended at =", dt_string)
        print("[Get Award Nominees] duration:",str(endTime-startTime))
        if MOCK_AWARD_NOMINEES:
            print("Mocking award nominees")
            nominees = gg_apifake.get_nominees(year)
            for category in nominees.keys():
                for award in self.awards:
                    if award.award_category.award_name == category:
                        award.SetNominees(nominees[category])
        else:
            print("Not mocking award nominees")
            for award in self.awards:
                award.SetNominees(self.get_nominees_for_award(award))

    def get_nominees_for_award(self, award):
        return AwardNameToNominees(self.tweets,award)

    def get_awards(self, year):
        return self.awards

    def get_award_winners(self, year):
        startTime = datetime.now()
        dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
        print("[Get Award Winners] process started at =", dt_string)
        
        if MOCK_AWARD_WINNERS:
            print("Mocking award winners")
            winners = gg_apifake.get_winner(year)
            for category in winners.keys():
                for award in self.awards:
                    if award.award_category.award_name == category:
                        award.SetWinner(winners[category])

        else:
            print("Not mocking award winners")
            for award in self.awards:
                award.SetWinner(self.get_winner_for_award(award))

        endTime = datetime.now()
        dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
        print("[Get Award Winners] process ended at =", dt_string)
        print("[Get Award Winners] duration:",str(endTime-startTime))


    def get_winner_for_award(self, award):
        return AwardNameToWinners(self.tweets,award)
    
    def get_red_carpet(self, year):
        startTime = datetime.now()
        dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
        print("[Get Red Carpet] process started at =", dt_string)

        self.red_carpet_results = find_redcarpet(self.tweets)

        endTime = datetime.now()
        dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
        print("[Get Red Carpet] process ended at =", dt_string)
        print("[Get Red Carpet] duration:",str(endTime-startTime))
        

    def get_hosts(self, year):
        startTime = datetime.now()
        dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
        print("[Get Hosts] process started at =", dt_string)

        if MOCK_HOSTS:
            print("Mocking hosts")
            self.hosts = gg_apifake.get_hosts(year)
        else:
            print("Not mocking hosts")
            self.hosts = find_host(self.tweets)

        endTime = datetime.now()
        dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
        print("[Get Hosts] process ended at =", dt_string)
        print("[Get Hosts] duration:",str(endTime-startTime))       


    def export_hosts(self):
        return self.hosts

    def export_presenters(self):
        presenters = {}
        for award in self.awards:
            presenters[award.award_category.award_name] = award.presenters
        return presenters

    def export_nominees(self):
        nominees = {}
        for award in self.awards:
            nominees[award.award_category.award_name] = award.nominees
        return nominees

    def export_winners(self):
        winners = {}
        for award in self.awards:
            winners[award.award_category.award_name] = award.winner
        return winners

    def export_award_categories(self):
        awards = {}
        for award in self.awards:
            awards[award.award_category] = award
        return awards
    
    def export_red_carpet(self):
        return self.red_carpet_results

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', dest='year', action='store', help='the year of the awards to get', nargs=1)
    parser.add_argument("--autograde", nargs='*', default=None, help='call the autograder which will output autograded information')
    parser.add_argument('--output_results', dest='output_results', action='store_true', help='output a human readable version of the awards that have been found')
    parser.add_argument('--save_json', dest='save_json', action='store_true', help='save the results of the autograder to a json file')

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

    startTime = datetime.now()
    dt_string = startTime.strftime("%d/%m/%Y %H:%M:%S")
    print("[RUNNER] process started at =", dt_string)

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
        
        autograder.main([year], functions)

    if args.output_results:
        if not autograde:
            runner.get_award_categories(year)
            runner.get_hosts(year)
            runner.get_all_award_presenters(year)
            runner.get_award_nominees(year)
            runner.get_award_winners(year)
            awards = runner.get_awards(year)
        else:
            awards = gg_api.get_award_objects(year)
        runner.get_red_carpet(year)
                
        print("Hosts: " + str(runner.export_hosts()) + "\n")
        for award in awards:
            print(str(award) + "\n")

        print("Red Carpet Results:")
        red_carpet_results = runner.export_red_carpet()
        print("\tThree Most Discussed: " + str(red_carpet_results["Three Most Discussed"]))
        print("\tBest Dressed: " + str(red_carpet_results["Best Dressed"]))
        print("\tWorst Dressed: " + str(red_carpet_results["Worst Dressed"]))
        print("\tMost Controversial: " + str(red_carpet_results["Most Controversial"]))
    
    if args.save_json:
        if not autograde and not args.output_results:
            runner.get_award_categories(year)
            runner.get_hosts(year)
            runner.get_all_award_presenters(year)
            runner.get_award_nominees(year)
            runner.get_award_winners(year)

            awards = runner.get_awards(year)
            hosts = runner.export_hosts()
            presenters = runner.export_presenters()
            nominees = runner.export_nominees()
            winners = runner.export_winners()
        elif autograde and not args.output_results:
            awards = gg_api.get_award_objects(year)
            hosts = gg_api.get_hosts(year)
            presenters = gg_api.get_presenters(year)
            nominees = gg_api.get_nominees(year)
            winners = gg_api.get_winner(year)
        elif args.output_results:
            awards = runner.get_awards(year)
            hosts = runner.export_hosts()
            presenters = runner.export_presenters()
            nominees = runner.export_nominees()
            winners = runner.export_winners()
        else:
            runner.get_award_categories(year)
            runner.get_hosts(year)
            runner.get_all_award_presenters(year)
            runner.get_award_nominees(year)
            runner.get_award_winners(year)

            awards = runner.get_awards(year)
            hosts = runner.export_hosts()
            presenters = runner.export_presenters()
            nominees = runner.export_nominees()
            winners = runner.export_winners()

        data = {
            "Hosts": hosts,
        }
        for award in awards:
            data[award.award_category.award_name] = {
                "Nominees": award.nominees,
                "Presenters": award.presenters,
                "Winner": award.winner
            }
        with open('gg_{}_generated_answers.json'.format(year), 'w') as outfile:
            json.dump(data, outfile)

    endTime = datetime.now()
    dt_string = endTime.strftime("%d/%m/%Y %H:%M:%S")
    print("[RUNNER] process ended at =", dt_string)
    print("[RUNNER] duration:",str(endTime-startTime))
    


