from bs4 import BeautifulSoup
import requests
import re
import csv


def findMovies():

    movies = []
    for start in range(1, 2500, 250):
        # url = f"https://www.imdb.com/search/title/?release_date=1900-01-01,2022-12-31&view=simple&sort=num_votes,desc&count=250&start={start}&ref_=adv_nxt"
        url = f"https://www.imdb.com/search/title/?title_type=feature,tv_movie,tv_series,tv_special,tv_miniseries,documentary,short,video,tv_short&release_date=2000-01-01,2022-12-31&view=simple&count=250&sort=num_votes,desc&start={start}&ref_=adv_nxt"
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

def findTV():
    # https://www.imdb.com/search/title/?title_type=tv_movie,tv_series,tv_miniseries&release_date=2000-01-01,2022-12-31&sort=num_votes,desc&count=250
    shows = []
    for start in range(1, 2500, 250):
        # url = f"https://www.imdb.com/search/title/?release_date=1900-01-01,2022-12-31&view=simple&sort=num_votes,desc&count=250&start={start}&ref_=adv_nxt"
        url = f"https://www.imdb.com/search/title/?title_type=tv_movie,tv_series,tv_miniseries&release_date=2000-01-01,2022-12-31&sort=num_votes,desc&count=250&start={start}&ref_=adv_nxt"
        # query the page
        html = requests.get(url)
        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(html.text, "html.parser")

        # hyperlinks = soup.select("a[href*=title]")
        hyperlinks = soup.find_all("a", href=re.compile("title/tt"))

        # print(hyperlinks)
        
        for link in hyperlinks:
            if link.text != "" and link.text != "\n" and link.text != " \n" and link.text != "  \n" and link.text != "X":
                shows.append(link.text)
    return shows

def findPeople():
    # this also includes actresses
    people = []
    for start in range(1, 3001, 100):
        # WORK IN Progress
        url = f"https://www.imdb.com/search/name/?birth_date=1920-01-01,2022-12-31&count=100&start={start}&ref_=rlm"
        
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")

        hyperlinks = soup.find_all("a", href=re.compile("name/nm"))

        for link in hyperlinks:
            if link.text != "" and link.text != "\n" and link.text != " \n" and link.text != "  \n":
                # remove the \n at end of name
                actor_name = link.text[:-1]
                # strip extra spaces
                people.append(actor_name.strip())

    url = f"https://www.imdb.com/list/ls048362057/?count=100&ref_=rlm"

    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")

    hyperlinks = soup.find_all("a", href=re.compile("name/nm"))

    for link in hyperlinks:
        if link.text != "" and link.text != "\n" and link.text != " \n" and link.text != "  \n":
            # remove the \n at end of name
            singer_name = link.text[:-1]
            # strip extra spaces
            people.append(singer_name.strip())
    
    return people


# people = findPeople()
tv = findTV()


# with open('people.csv', 'w', newline='') as myfile:
#      wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#      wr.writerow(people)

# merge TV into movies.csv if the entry is not already in movies.csv
with open('movies.csv', 'r') as file:
    reader = csv.reader(file)
    movies = list(reader)[0]
    for show in tv:
        if show not in movies:
            movies.append(show)


with open('movies.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(movies)