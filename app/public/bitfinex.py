#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from json import loads
from datetime import datetime
import settings
import logging
import requests
import random
import time
import utils

class BitFinex_Market(object):
    """Bitfinex Market Data"""
    def __init__(self):
        self.api_url = settings.BITFINEX_API_URL
        self.exchange = 'bitfinex'
        self.products = {'ethusd':'eth.bitfinex.ticker',
                         'btcusd':'btc.bitfinex.ticker'}
        if settings.BITFINEX_API_URL[-1] == "/":
            self.api_url = settings.BITFINEX_API_URL[:-1]

    def normalize_ticker(self,data):
        clean_data = dict()
        clean_data["ask"] = float(data["ask"])
        clean_data["bid"] = float(data["bid"])
        clean_data["price"] = float(data["last_price"])
        clean_data["volume"] = float(data["volume"])

        return clean_data

    def get_ticker(self,product):
        """Get current tick"""
        now = datetime.utcnow()
        r = requests.get(self.api_url + '/v1/pubticker/' + product, timeout=settings.API_TIMEOUT)
        data = loads(r.text)
        if 'last_price' in data:
            data = self.normalize_ticker(data)
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
