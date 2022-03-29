# coding=utf-8

import requests as req
from bs4 import BeautifulSoup


class ParserApp2top:    # main class
    """
    App2top.com site parser script.
    Collects articles issued by the search query,
    taking into account pagination.

    In: pattern - either 'My.Com' or 'Google' or whatever
    Out: article title, article url.

    'pattern' required variable*
    """
    def run(self, pattern):     # function start
        return self.parser(self.search(pattern))    # Output

    @staticmethod
    def search(pattern):    # search function for 'pattern'
        page = 1    # pagination start
        result = []     # query result
        while page:     # site pagination loop
            URL = req.get(f'https://app2top.ru/page/{page}?s={pattern}')    # request generation
            if URL.reason == 'Not Found':   # Request response received with 404 or Not Found
                break   # exits the loop
            result.append(URL)  # add the resulting site form to the result
            page += 1   # go to new page
        return result   # output of the results

    @staticmethod
    def parser(url_raw):    # parsing function
        result = []     # query result
        for url in url_raw:     # loop through the list
            soup = BeautifulSoup(url.text, 'lxml')  # forming a response from the site into a reading format
            for article in soup.findAll("a", {"class": "post-preview-pic no-shrink"}):
                # search for required HTML tags with class parameter
                result.append({'title': article['title'], 'url': 'https:'+article['href']})
                # adds title and url to result
        return result   # output of the results


if __name__ == "__main__":
    parser = ParserApp2top()    # calling the site parser class
    print(parser.run(pattern='My.Com'))     # print the result of the query to the console
