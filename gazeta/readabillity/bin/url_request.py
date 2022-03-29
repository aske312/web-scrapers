# -*- coding: utf-8 -*-

import requests
import re
import os
from bs4 import BeautifulSoup


class ParserNews:
    """
    ParserNews - parser of news sites, accepts url to break it down before generating a text report.
    :argument - url
    """
    def __init__(self, url):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36'
        }
        self.url = url

    def run(self):
        headline, text = self.url_parser()
        self.directory_create(path=self.name_file())
        self.with_file(file_name=self.name_file(), headline=headline, text=self.text_convector(text))

    def url_parser(self):
        s = requests.Session()
        response = s.get(url=self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        headline = soup.find('h1')
        text = soup.find_all('p')
        return headline, text

    def text_convector(self, text):
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

    def name_file(self):
        if re.findall(r'https://www.', self.url):
            name_file = self.url.replace('https://www.', '')
        elif re.findall(r'https://', self.url):
            name_file = self.url.replace('https://', '')
        elif re.findall(r'http://', self.url):
            name_file = self.url.replace('http://', '')
        else:
            raise ValueError
        if name_file[-1] == '/':
            name_file = name_file[:-1] + '.txt'
        else:
            name_file = str(name_file).replace('.shtml', '.txt')
        return name_file

    def directory_create(self, path):
        path = path.split('/')
        directory = os.getcwd()
        for new in path[:-1]:
            directory = directory + '/' + new
        if os.path.isdir(directory):
            directory = directory + '/' + path[-1]
        else:
            os.makedirs(directory)

    def with_file(self, file_name='text.txt', headline=None, text=None):
        with open(file_name, 'w+') as new_file:
            new_file.write('\t')
            for line in headline.text.split()[:-1]:
                new_file.write(line + ' ')
            new_file.write(''.join(headline.text.split()[-1:]) + '.\n\n')
            for line in text:
                if len(line) > 80:
                    filter_text = lambda A, n=(len(line.split()) //
                                               (len(line) // 80 + 1)): [A[i:i + n] for i in range(0, len(A), n)]
                    new_file.write('\t')
                    for st in filter_text(line.split()):
                        new_file.write(' '.join(st) + '\n')
                    new_file.write('\n')
                else:
                    new_file.write('\t' + line + '\n')
            new_file.close()


def get_text_form(url='https://www.gazeta.ru/social/news/2021/11/28/n_16931005.shtml'):
    ParserNews(url=url).run()
