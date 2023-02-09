# CS 337 - Project 1
### By: Gabe Bider, Spencer Rothfleisch, Eli Barlow, and Isaac Miller


## How to Run
To Run:
Create the virtual environment:
```bash
python3 -m venv env
```
Activate the virtual environment:
```bash
source env/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```
or
```bash
pip3 install -r requirements.txt
```

To Configure the mocks edit the .env file
By default the mocks are set to the following:

```bash
MOCK_AWARD_CATEGORIES=False
MOCK_AWARD_PRESENTERS=False
MOCK_AWARD_WINNERS=False
MOCK_AWARD_NOMINEES=False
MOCK_HOSTS=False
MOCK_RED_CARPET=False
MOCK_SENTIMENT=False
```
Turning these on will enable the mocks and will use the data from gg_apifake.py

To Run the program:
Supplying no arguments will run the program with the default values
You need supply --output_results in order to get console output results
Adding --save_json will save the json files to gg_{year}_generated_answers.json in the format for the auto grader


```bash
# This will print the results and save the json files
python Runner.py --output_results --year 2013 --save_json

# This will save the json files
python Runner.py --year 2013 --save_json

# This will print the results
python Runner.py --output_results --year 2013
```

## Scraping Data
In order to scrape our data from IMDB, we made a file scraper.py

The requirements for the scraper are installed with the requirements.txt file


## What did we do

### Main Requirements
- [x] - Hosts
- [x] - Award Categories
- [x] - Presenters (not 100% accurate)
- [x] - Nominees (not 100% accurate)
- [x] - Winners

### Extras
- [x] - Red Carpet
    - [x] Best Dressed
    - [x] Worst Dressed
    - [x] Most Controversial
    - [x] Three Most Discussed
- [x] - Sentiment Analysis
    - [x] Sentiments regarding hosts
    - [x] most positive winner
    - [x] least positive winner

## Other notes
- Our code groups together similar awards into one award name with a set of aliases. These can be found in `award_aliases.json`. Because of this, it is possible that code may not work will all the subparts when mocking Award Categories.
- The files `TimeToJson.py` and `IntervalTester.py` create plots in the folder `test_tweets_time/` that provide interesting visualizations about where tweets about certain awards fall on a chronological scale (we used these to identify presenters and nominees)
- The files in `saved_jsons/` are for internal use of the award category recognition function.
- The main Runner takes on average 4.5 minutes to run on a Macbook Pro M1 chip (with video/other programs running in the background). The extra sections add around 30 seconds in total.

## [Our GitHub Repository](https://github.com/gabebider/cs337-proj1)
