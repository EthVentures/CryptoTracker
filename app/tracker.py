#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@authors: dconroy
          avelkoski
"""
from elasticsearch import Elasticsearch, helpers
from public.bitfinex import BitFinex_Market
from public.bitmex import BitMex_Market
from public.bittrex import BitTrex_Market
from public.gdax import GDAX_Market
from public.gemini import Gemini_Market
from public.kraken import Kraken_Market
from public.okcoin import OKCoin_Market
from public.poloniex import Poloniex_Market
from dotenv import Dotenv
from time import sleep
import logging
import schedule
import settings
import utils
import random
import time

def main():
    logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',level=settings.LOGLEVEL)
    es = Elasticsearch(settings.ELASTICSEARCH_CONNECT_STRING)

    logging.info('Market Refresh Rate: ' + str(settings.MARKET_REFRESH_RATE) + ' seconds.')
    logging.info('Initial Sleep: ' + str(settings.INITIAL_SLEEP) + ' seconds.')

    sleep(settings.INITIAL_SLEEP)
    logging.info('Application Started.')
    #supported_exchanges = [BitFinex_Market(), BitMex_Market(), BitTrex_Market(), GDAX_Market(), Gemini_Market(), Kraken_Market(), OKCoin_Market(), Poloniex_Market()]
    exchanges = [BitFinex_Market(), BitMex_Market(), BitTrex_Market(), GDAX_Market(), Gemini_Market(), Kraken_Market(), OKCoin_Market(), Poloniex_Market()]


    #print active exchanges and create indexes in kibana based on products listed in each market
    for exchange in exchanges:
        logging.info(exchange.exchange + ': activated and indexed.')
        for product, kibana_index in exchange.products.iteritems():
            utils.create_index(es, kibana_index)

    logging.warn('Initiating Market Tracking.')

    #Record Ticks
    while True:
        sleep(settings.MARKET_REFRESH_RATE)
        try:
            for exchange in exchanges:
                exchange.record_ticker(es)

        except Exception as e:
            logging.warning(e)
            sleep(settings.RETRY_RATE)

if __name__ == '__main__':
    main()
