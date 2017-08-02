#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from json import loads
from datetime import datetime, timedelta
import settings
import logging
import requests
import utils

class GDAX_Market(object):
    """GDAX Market Data"""
    def __init__(self):
        self.api_url = settings.GDAX_API_URL
        self.exchange = 'gdax'
        self.products = {'ETH-USD': 'eth.gdax.ticker',
                         'BTC-USD': 'btc.gdax.ticker'}
        if settings.GDAX_API_URL[-1] == "/":
            self.api_url = settings.GDAX_API_URL[:-1]

    def normalize_ticker(self, data):
        for key in data:
            if key == 'time':
                data[key] = datetime.strptime(
                    data[key], "%Y-%m-%dT%H:%M:%S.%fZ")
            elif key == 'trade_id':
                data[key] = int(data[key])
            else:
                data[key] = float(data[key])

        return data

    def get_ticker(self, product):
        """Get current tick"""
        data = dict()
        now = datetime.utcnow()
        r = requests.get(self.api_url + '/products/' + product + '/ticker', timeout=settings.API_TIMEOUT)
        data = loads(r.text)
        if 'price' in data:
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
