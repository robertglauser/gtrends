from datetime import datetime, timedelta, time
from pytrends.request import TrendReq
import pandas as pd
import os
import csv
import time

path = '/Users/Robert/PycharmProjects/gtrends'
os.chdir(path)

maxstep = 269
overlap = 40
step = maxstep - overlap + 1
start_date = datetime(2014, 12, 9).date()
counter = 0


def createDailyDataExtract(kw: object) -> object:
    global counter
    localcounter = counter
    counter = counter + 1
    filename = '/results/result-'+str(localcounter)+'.csv'
    print(filename)
    kw_list = kw
    print(kw_list)
    pytrend = TrendReq()

    today = datetime.today().date()
    old_date = today

    new_date = today - timedelta(days=step)

    timeframe = new_date.strftime('%Y-%m-%d') + ' ' + old_date.strftime('%Y-%m-%d')
    pytrend.build_payload(kw_list=kw_list, timeframe=timeframe, geo='')
    interest_over_time_df = pytrend.interest_over_time()

    while new_date > start_date:

        old_date = new_date + timedelta(days=overlap - 1)

        new_date = new_date - timedelta(days=step)
        if new_date < start_date:
            new_date = start_date

        timeframe = new_date.strftime('%Y-%m-%d') + ' ' + old_date.strftime('%Y-%m-%d')
        print(timeframe)

        pytrend.build_payload(kw_list=kw_list, timeframe=timeframe)
        temp_df = pytrend.interest_over_time()

        if (temp_df.empty):
            raise ValueError(
                'Google sent back an empty dataframe. Possibly there were no searches at all during the this period! Set start_date to a later date.')
        for kw in kw_list:
            beg = new_date
            end = old_date - timedelta(days=1)

            for t in range(1, overlap + 1):
                if temp_df[kw].iloc[-t] != 0:
                    scaling = interest_over_time_df[kw].iloc[t - 1] / temp_df[kw].iloc[-t]
                    break
                elif t == overlap:
                    print('Did not find non-zero overlap, set scaling to zero! Increase Overlap!')
                    scaling = 0
            temp_df.loc[beg:end, kw] = temp_df.loc[beg:end, kw] * scaling
        interest_over_time_df = pd.concat([temp_df[:-overlap], interest_over_time_df])

    interest_over_time_df.to_csv('/Users/Robert/PycharmProjects/gtrends'+filename)
    time.sleep(1)


with open('newkeywords.csv', 'r') as keywordfile:
    keywordreader = csv.reader(keywordfile)
    for kw in keywordreader:
        createDailyDataExtract(kw)
