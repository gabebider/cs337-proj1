from Award import Award
import csv
from AwardCategory import AwardCategory
from aliases import get_aliases

# gets the nominees from the csv file, for testing purposes
def getNominees():
    # Open the CSV file and read the data into a list
    with open("golden_globe_awards.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Filter the data to only include films from 2013
    filtered_data = [row for row in data if row[1] == "2013"]

    # Create a dictionary to store the award information
    awards = {}

    # Loop through the filtered data and add the award information to the dictionary
    for row in filtered_data:
        category = row[3].lower()
        nominee = row[4].lower().strip()
        film = row[5].lower().replace("\t", "").strip()
        win = row[6]

        # Check if the award already exists in the dictionary
        if category not in awards:
            # If it doesn't, create a new entry for the award
            awards[category] = {"winner": None, "nominees": []}

        # Add the nominee information to the dictionary
        awards[category]["nominees"].append(
            {"nominee": nominee, "film": film})

        # If the nominee won, update the winner property
        if win == "True":
            awards[category]["winner"] = {"nominee": nominee, "film": film}

    # print(awards)
    return awards

# returns list of awards, used for testing purposes
def getAwards():
    with open("golden_globe_awards.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Filter the data to only include films from 2013
    filtered_data = [row for row in data if row[1] == "2013"]
    awards = []
    addedAwards = []
    aliases = get_aliases()

    # create list of awards
    for row in filtered_data:
        if row[3] not in addedAwards:
            addedAwards.append(row[3])
            awardStruct = Award(AwardCategory(row[3].lower()))
            awardStruct.award_category.aliases = aliases[row[3].lower()]
            print(awardStruct.award_category.aliases)
            awards.append(awardStruct)
    return awards

# finds the nominees given a list of awards
def findNominees(awards):
    for award in awards:
        print(award.__str__())

findNominees(getAwards())