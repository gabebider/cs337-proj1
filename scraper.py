from bs4 import BeautifulSoup
import requests
import re
import csv


def findMovies():

    movies = []
    for start in range(1, 10001, 250):
        url = f"https://www.imdb.com/search/title/?release_date=1900-01-01,2022-12-31&view=simple&sort=num_votes,desc&count=250&start={start}&ref_=adv_nxt"
        # query the page
        html = requests.get(url)
        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(html.text, "html.parser")

        # hyperlinks = soup.select("a[href*=title]")
        hyperlinks = soup.find_all("a", href=re.compile("title/tt"))

        # print(hyperlinks)
        
        for link in hyperlinks:
            if link.text != "" and link.text != "\n" and link.text != " \n" and link.text != "  \n":
                movies.append(link.text)


    return movies



def findActors():
    # this also includes actresses
    actors = []
    for start in range(1, 10001, 100):
        # WORK IN Progress
        url = f"https://www.imdb.com/search/name/?birth_date=1900-01-01,2022-12-31&count=100&start={start}&ref_=rlm"
        
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")

        hyperlinks = soup.find_all("a", href=re.compile("name/nm"))

        for link in hyperlinks:
            if link.text != "" and link.text != "\n" and link.text != " \n" and link.text != "  \n":
                # remove the \n at end of name
                actor_name = link.text[:-1]
                # strip extra spaces
                actors.append(actor_name.strip())
    
    return actors


movies = findMovies()
actors = findActors()

with open('movies.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(movies)

with open('actors.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(actors)