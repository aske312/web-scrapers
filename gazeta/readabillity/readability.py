# -*- coding: utf-8 -*-
import argparse
from bin.url_request import get_text_form

parser = argparse.ArgumentParser(description='Urls of the site for preparing the reading form')
parser.add_argument("-u", "--url", type=str, help="A news site or site for composing a readability form is expected.")
args = parser.parse_args()
answer = args.url

if args.url:
    get_text_form(url=args.url)
    print('Files is successful!')
else:
    print(answer)
