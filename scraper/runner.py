# -*- coding: utf-8 -*-

import time
import requests
from pyparsing import *
from bs4 import BeautifulSoup
from config import *


class ScraperRun:
    def __init__(self, source):
        self._list = source
        self._headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36'
        }

    def _requests(self, url):
        s = requests.Session()
        response = s.get(url=url, headers=self._headers)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
        else:
            raise ResponseNotOk('Response not ok, maybe time out.')
        return soup

    def _pars_source(self, site):
        if re.search('.gazeta.ru/', site):
            result = self._requests(site).findAll("a", {"class": "b_ear-image"})
            site = site.replace('/news/', '')
        elif re.search('/lenta.ru/', site):
            result = self._requests(site).findAll("a", {"class": "card-full-news _parts-news"})
            site = site.replace('/parts/news/', '')
        elif re.search('/vc.ru/', site):
            result = self._requests(site).findAll("a", {"class": "content-link"})
            site = site.replace('/new/all', '')
        else:
            raise UnknownSource("unknown news source, can't process, check source!")
        for line in result:
            if re.search('https:/', line['href']):
                yield line['href']
            else:
                yield site + line['href']

    def _pars_url(self, url_pool):
        for url in url_pool:
            text_box = []
            soup = self._requests(url)  # 'https://www.gazeta.ru/army/news/2022/06/23/17988770.shtml')
            headline = soup.find('h1')
            text = soup.find_all('p')
            for p_tag in text:
                text_box.append(p_tag.text)
            article = {'headline': headline.text, 'text_box': text_box}
            print(article)

    def _login_requests(self, url_pool):
        log = open('logs/requests.log', 'a')
        log.write(url_pool)

    @log_errors
    def start(self):
        start_time = time.time()
        url_pool = []
        for source in SOURCE:
            for pool in self._pars_source(source):
                url_pool.append(pool)
        # print(url_pool)
        print(self._login_requests(url_pool))
        # self._pars_url(url_pool)
        print("--- %s seconds ---" % (time.time() - start_time))


ScraperRun(SOURCE).start()
