#!.venv/bin/python3

import argparse
import datetime
import time
import csv
import os

import requests

from db import DB_Helper

BASE_URL = "https://api.exmo.com/v1/order_book/"
PAIRS = ('BTC_USD', 'ETH_USD', 'ETH_BTC',)
DELAY = 10  # seconds delay between requests
FMT_ROW = '{:^20}'


def get_best_pair(pairs):
    """
    Function to get the book of current orders on the currency pair

     pairs     - list of currency pair, e.g. ['BTC_USD', 'ETH_USD', 'ETH_BTC']
     best_pair - dictionary of minimum sell price and maximum buy price for each pair
                  'datetime' - datetime when the request was sent, format %Y-%m-%d %H:%M:%S
                  'PAIR_ASK' - the minimum sell price for pair, e.g. best_pair[BTC_USD_ASK] = 5735
                  'PAIR_BID' - the maximum buy  price for pair, e.g. best_pair[BTC_USD_BID] = 5711.01
    """
    best_pair = {}
    params = {'pair': ','.join(pairs)}
    try:
        r = requests.get(BASE_URL, params=params)
    except requests.exceptions.RequestException as e:
        print('Connection error: ', e)
    else:
        if r.status_code == 200:
            best_pair['datetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for pair in r.json().keys():
                best_pair[pair+'_ASK'] = float(r.json()[pair]['ask_top'])
                best_pair[pair+'_BID'] = float(r.json()[pair]['bid_top'])
        else:
            print('Connection error, status code: ', r.status_code)
    return best_pair


def save2csv(best_pair, filename):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if not os.path.exists(path):
        with open(path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted(best_pair.keys(), reverse=True), delimiter='|')
            writer.writeheader()

    with open(path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=sorted(best_pair.keys(), reverse=True), delimiter='|')
        writer.writerow(best_pair)


def main():
    parser = argparse.ArgumentParser(description='Get the book of current orders on the currency pair and save to database and/or file [*.csv]')
    parser.add_argument('-f', '--filename', action='store', dest='filename',
                        help='save table to filename, e.g. *.csv', type=str)
    parser.add_argument('-d', '--database', action='store_true', dest='database',
                        help='save to database')
    args = parser.parse_args()

    print_header = True
    try:
        if args.database:
            db = DB_Helper()
        while True:
            best_pair = get_best_pair(PAIRS)
            if print_header:
                header = '|'.join(FMT_ROW.format(k) for k in sorted(best_pair.keys(), reverse=True))
                print(header)
                print('-'*len(header))
                print_header = False
            print('|'.join(FMT_ROW.format(best_pair[k]) for k in sorted(best_pair.keys(), reverse=True)))
            if args.filename:
                save2csv(best_pair, filename=args.filename)
            if args.database:
                db.add(best_pair)
            time.sleep(DELAY)
    finally:
        if args.database:
            db.destroy()


if __name__ == '__main__':
    main()
