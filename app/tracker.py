#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch, helpers
from exchange_harness import ExchangeHarness
import logging
# import schedule
import settings
import utils
import random
import time
from concurrent.futures import ThreadPoolExecutor
from time import sleep

def main():
    logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',level=settings.LOGLEVEL)
    es = Elasticsearch(settings.ELASTICSEARCH_CONNECT_STRING)

    logging.info('Market Refresh Rate: ' + str(settings.MARKET_REFRESH_RATE) + ' seconds.')
    logging.info('Initial Sleep: ' + str(5) + ' seconds.')


    logging.info('Application Started.')
    #supported_exchanges = [BitFinex_Market(), BitMex_Market(), BitTrex_Market(), GDAX_Market(), Gemini_Market(), Kraken_Market(), OKCoin_Market(), Poloniex_Market()]
    tmp = ['bitstamp', 'gdax', 'kraken', 'gemini']
    exchanges = [ExchangeHarness(x) for x in tmp]


    #print active exchanges and create indexes in kibana based on products listed in each market
    for exchange in exchanges:
        logging.info(exchange.exchange_id + ': activated and indexed.')
        for product, kibana_index in exchange.products.items():
            utils.create_index(es, kibana_index)

    logging.warn('Initiating Market Tracking.')

    #Record Ticks
    while True:
        with ThreadPoolExecutor(max_workers=5) as executor:
            try:
                sleep(settings.MARKET_REFRESH_RATE)
                executor.map(lambda ex: ex.record_ticker(es), exchanges)
                logging.info("added another ticker record")
            except Exception as e:
                logging.warning(e)
                sleep(settings.RETRY_RATE)




if __name__ == '__main__':

    main()
