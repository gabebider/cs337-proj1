# CS 337 - Project 1
### By: Gabe Bider, Spencer Rothfleicsch, Eli Barlow, and Isaac Miller

To Run:

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
You need to either supply --output_results or --autograde in order to get results

```bash
python Runner.py --output_results --autograde --year 2013
```
