# -*- coding: utf-8 -*-

import requests
import re
import os
import json
from pyparsing import *
from bs4 import BeautifulSoup


class UrlGazetaRu:
    """
    ParserNews - parser of news sites, accepts url to break it down before generating a text report.
    :argument - url
    """

    def __init__(self, url):
        self._url = url
        self._headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36'
        }
        self.result = {"articles": []}
        # with open('dump.json', 'r') as dumpfile:
        #     self.result = json.loads(dumpfile.read())

    def _search(self, url):
        raw_url = str(url)
        if re.search('gazeta.ru', raw_url):
            if re.search('/(n_)?\d+.s?html', raw_url):
                key, url, headline, text = self._parser(raw_url)
                self.result['articles'].append({key: [url, headline, text]})
            else:
                for url in self._parser_articles(raw_url):
                    self._url = url
                    key, url, headline, text = self._parser(url)
                    self.result['articles'].append({key: [url, headline, text]})
            return self.result
        else:
            raise ValueError

    def _parser_articles(self, raw_url):
        s = requests.Session()
        response = s.get(url=raw_url, headers=self._headers)
        soup = BeautifulSoup(response.text, 'lxml')
        div_article = soup.findAll("div", {"class": "b_ear-title"})
        pattern = Regex(r'<a href="([\:\/\w\d\.]+)">').sub(r"\1")
        url_array = []
        for found in pattern.searchString(div_article):
            for url in found:
                if re.search('https://www.', url):
                    url_array.append(url)
                else:
                    url = 'https://www.gazeta.ru' + url
                    url_array.append(url)
        return url_array

    def _parser(self, url):
        s = requests.Session()
        response = s.get(url=url, headers=self._headers)
        soup = BeautifulSoup(response.text, 'lxml')
        headline = soup.find('h1')
        text = soup.find_all('p')
        return self._keygen(self._url), url, headline.text, self._text_convector(text)

    def _text_convector(self, text):
        text_line = []
        for line in text:
            if line.a:
                url_txt = line.a.text + ' [' + line.a['href'] + ']'
                txt = line.text.replace(line.a.text, url_txt)
                txt = txt.replace('\xa0', ' ')
                text_line.append(txt)
            else:
                txt = line.text.replace('\xa0', ' ')
                text_line.append(txt)
        return text_line

    def _keygen(self, raw_url):
        return int(re.sub(r'(^.+/)(\w_)?(\d{5,})(.\w+$)', r'\3', raw_url))

    def runer(self):
        article = self._search(self._url)
        print(article)
        # print(self.result)
        # with open('dump.json', 'w+') as dumpfile:
        #     json.dump(self.result, dumpfile)


def get_text_form(url='https://www.gazeta.ru/social/news/2021/11/28/n_16931005.shtml'):
    UrlGazetaRu(url=url).runer()


# get_text_form('https://www.gazeta.ru/news/123213.html')
get_text_form('https://www.gazeta.ru/news/')
# get_text_form('https://www.gazeta.ru/')
# get_text_form('https://www.gazeta.ru/social/news/2021/11/28/n_16931005.shtml')
