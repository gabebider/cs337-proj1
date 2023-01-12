from bs4 import BeautifulSoup
import requests
import re


def findMovies():

    for start in range(1, 10001, 250):
        url = f"https://www.imdb.com/search/title/?release_date=1900-01-01,2022-12-31&view=simple&sort=num_votes,desc&count=250&start={start}&ref_=adv_nxt"
        # query the page
        html = requests.get(url)
        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(html.text, "html.parser")

        # hyperlinks = soup.select("a[href*=title]")
        hyperlinks = soup.find_all("a", href=re.compile("title/tt"))

        # print(hyperlinks)
        movies = {}
        for link in hyperlinks:
            if link.text != "" and link.text != "\n" and link.text != " \n" and link.text != "  \n":
                movies[link.text] = 1
        
    print(movies)

findMovies()