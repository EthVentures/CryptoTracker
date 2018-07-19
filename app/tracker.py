#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@authors: dconroy
          avelkoski
"""
from elasticsearch import Elasticsearch, helpers
from public.bitfinex import BitfnexMarket
from public.bitmex import BitMexMarket
from public.bittrex import BitTrexMarket
from public.gdax import GDAXMarket
from public.gemini import GeminiMarket
from public.kraken import KrakenMarket
from public.okcoin import OkCoinMarket
from public.poloniex import PloloniexMarket
from dotenv import Dotenv
from time import sleep
import logging
import schedule
import settings
import utils
import random
import time

support_exchange = [
    BitTrexMarket,
    BitMexMarket,
    GDAXMarket,
    GeminiMarket,
    KrakenMarket,
    OkCoinMarket,
    PloloniexMarket,
    BitfnexMarket
]


def main():
    logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',level=settings.LOGLEVEL)
    es = Elasticsearch(settings.ELASTICSEARCH_CONNECT_STRING)

    logging.info('Market Refresh Rate: ' + str(settings.MARKET_REFRESH_RATE) + ' seconds.')
    logging.info('Initial Sleep: ' + str(settings.INITIAL_SLEEP) + ' seconds.')

    sleep(settings.INITIAL_SLEEP)
    logging.info('Application Started.')
    exchanges = [ex() for ex in support_exchange]

    # print active exchanges and create indexes in kibana based on products listed in each market
    for exchange in exchanges:
        logging.info(exchange.exchange + ': activated and indexed.')
        for product, kibana_index in exchange.products.iteritems():
            utils.create_index(es, kibana_index)

    logging.warn('Initiating Market Tracking.')

    # Record Ticks
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
