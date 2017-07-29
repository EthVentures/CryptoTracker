#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@authors: dconroy
          avelkoski
"""
from elasticsearch import Elasticsearch, helpers
from public.gdax import GDAX_Market
from public.gemini import Gemini_Market
from dotenv import Dotenv
from time import sleep
import schedule
import logging
import settings
import utils
import random
import time

def main():
    logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',level=settings.LOGLEVEL)
    es = Elasticsearch(settings.ELASTICSEARCH_CONNECT_STRING)
    logging.info('Application Started.')
    exchanges = [GDAX_Market(),Gemini_Market()]
    for exchange in exchanges:
        logging.info(exchange.exchange + ': activated.')

    logging.info('Market Refresh Rate: ' + str(settings.MARKET_REFRESH_RATE) + ' seconds.')
    logging.info('Initial Sleep: ' + str(settings.INITIAL_SLEEP) + ' seconds.')
    logging.info('Application Started.')
    sleep(settings.INITIAL_SLEEP)

    logging.info('Checking Indices...')
    utils.create_indices(es, settings.INITIAL_INDEX_ARRAY)

    logging.warn('Initiating Market Tracking.')

    #Record Ticks
    while True:
        try:
            for exchange in exchanges:
                exchange.record_ticker(es)

            sleep(settings.MARKET_REFRESH_RATE)

        except Exception as e:
            logging.warning(e)
            sleep(settings.RETRY_RATE)

if __name__ == '__main__':
    main()
