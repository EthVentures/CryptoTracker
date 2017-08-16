#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from json import loads
from datetime import datetime, timedelta
import settings
import logging
import requests
import utils

class OKCoin_Market(object):
    """OKCOIN Market Data"""
    def __init__(self):
        self.api_url = settings.OKCOIN_API_URL
        self.exchange = 'okcoin'
        self.products = {'eth_usd': 'eth.okcoin.ticker',
                         'btc_usd': 'btc.okcoin.ticker'}
        if settings.OKCOIN_API_URL[-1] == "/":
            self.api_url = settings.OKCOIN_API_URL[:-1]

    def normalize_ticker(self, data):
        clean_data = dict()
        clean_data["ask"] = float(data["sell"])
        clean_data["bid"] = float(data["buy"])
        clean_data["price"] = float(data["last"])
        clean_data["volume"] = float(data["vol"])
        return clean_data

    def get_ticker(self, product):
        """Get current tick"""
        data = dict()
        now = datetime.utcnow()
        r = requests.get(self.api_url + '/ticker.do?symbol=' + product, timeout=settings.API_TIMEOUT)
        data = loads(r.text)
        logging.info(data)
        if 'ticker' in data:
            data = self.normalize_ticker(data['ticker'])
            logging.info(data)
            data["tracker_time"] = now
            data["exchange"] = self.exchange
            data["product"] = product
            return data
        else:
            raise ValueError("Invalid Response get_ticker from " + self.exchange)

    def record_ticker(self, es):
        """Record current tick"""
        for product in self.products:
            es_body=self.get_ticker(product)
            if 'price' in es_body:
                es.create(index=self.products[product], id=utils.generate_nonce(), doc_type='ticker', body=es_body)
            else:
                raise ValueError("Misformed Body for Elastic Search on " + self.exchange)
