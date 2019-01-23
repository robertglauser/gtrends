from datetime import datetime, timedelta, time
from pytrends.request import TrendReq
import pandas as pd
import os
import csv

path = '/Users/Robert/PycharmProjects/gtrends'
os.chdir(path)


def createmids(kw):
    filename='mids/' + 'midresults' + '.csv'
    print(filename)
    kw_list=kw
    print(kw_list)
    pytrend = TrendReq()


    ################# get mid
    a = pd.DataFrame(pytrend.suggestions(keyword=kw[0]))
    print(a)
    if not a.empty:
        b = a[(a['type'].str.lower().str.contains('company')) | (a['type'].str.lower().str.contains('corporation'))]
        if b['mid'].values.any():
            result = [b['mid'].values[0], b['title'].values[0], b['type'].values[0]]
            print(result)

with open('keywords.csv', 'r') as keywordfile:
    keywordreader = csv.reader(keywordfile)
    for kw in keywordreader:
        createmids(kw)
