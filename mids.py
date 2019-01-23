import csv
import os

import pandas as pd
from pytrends.request import TrendReq

path = '/Users/Robert/PycharmProjects/gtrends'
os.chdir(path)


def create_mid_from_keyword(keyword):
    save_mid_results = 'mids/midresults.csv'
    print(save_mid_results)

    print("\n\n\n")
    pytrend = TrendReq()

    # getMid
    mid_of_keyword = pd.DataFrame(pytrend.suggestions(keyword[0]))

    print("---------------- MID >>> ---------------")
    print(mid_of_keyword)
    print("---------------- <<< MID ---------------\n\n\n")

    if not mid_of_keyword.empty:
        mids_of_desired_types = mid_of_keyword[(mid_of_keyword['type'].str.lower().str.contains('bank')) | (mid_of_keyword['type'].str.lower().str.contains('company')) | (mid_of_keyword['type'].str.lower().str.contains('corporation'))]
        if mids_of_desired_types['mid'].values.any():
            mid_of_interest = [mids_of_desired_types['mid'].values[0], mids_of_desired_types['title'].values[0], mids_of_desired_types['type'].values[0]]

            print("---------------- MID OF INTEREST >>> ---------------")
            print(mid_of_interest[0])
            print(mid_of_interest[1])
            print(mid_of_interest[2])
            print("---------------- <<< MID OF INTEREST  ---------------\n\n\n")

            with open("results.csv", "a") as resultsFile:
                mid_entry = keyword[0] + ',' + mid_of_interest[0] + ',' + mid_of_interest[1] + ',' + mid_of_interest[2] + "\n"
                resultsFile.write(mid_entry)



with open('keywords.csv', 'r') as keywordFile:
    keywordReader = csv.reader(keywordFile)
    for kw in keywordReader:
        create_mid_from_keyword(kw)
