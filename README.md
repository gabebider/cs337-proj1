# CS 337 - Project 1
### By: Gabe Bider, Spencer Rothfleicsch, Eli Barlow, and Isaac Miller

To Run:
Activate the virtual environment:
```bash
source venv/bin/activate
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
```
Turning these on will enable the mocks and will use the data from gg_apifake.py

To Run the program:
Supplying no arguments will run the program with the default values
You need to either supply --output_results or --autograde in order to get output results
Adding --save_json will save the json files to gg_{year}_generated_answers.json in the format for the auto grader


```bash
# This will run the auto grader and print the results
python Runner.py --output_results --autograde --year 2013 --save_json

# This will run the auto grader and save the json files
python Runner.py --autograde --year 2013 --save_json

# This will run the auto grader and print the results
python Runner.py --output_results --autograde --year 2013

# This will save the json files in the format for the auto grader
python Runner.py --year 2013 --save_json
```

## What did we do

### Main Requirements
- [x] - Hosts
- [x] - Award Names
- [ ] - Presenters
- [x] - Nominees - some missing
- [x] - Winners

### Extras
- [x] - Red Carpet
    - [x] Best Dressed
    - [x] Worst Dressed
    - [x] Most Controversial
    - [x] Three Most Discussed

## [Our GitHub Repository](https://github.com/gabebider/cs337-proj1)