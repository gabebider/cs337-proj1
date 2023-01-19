
import csv


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
