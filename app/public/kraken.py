#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from json import loads
from datetime import datetime
import settings
import logging
import requests
import utils

class Kraken_Market(object):
    """ETH Kraken Market Data"""
    def __init__(self):
        self.api_url = settings.KRAKEN_API_URL
        self.exchange = 'kraken'
        self.products = {'XETHZUSD':'eth.kraken.ticker',
                         'XXBTZUSD':'btc.kraken.ticker'}
        if settings.KRAKEN_API_URL[-1] == "/":
            self.api_url = settings.KRAKEN_API_URL[:-1]

    def normalize_ticker(self,data):
        clean_data = dict()
        clean_data["ask"] = float(data["a"][0])
        clean_data["bid"] = float(data["b"][0])
        clean_data["price"] = float(data["c"][0])
        clean_data["size"] = float(data["c"][1])
        clean_data["volume"] = float(data["v"][1])
        return clean_data

    def get_ticker(self,product):
        """Get current tick"""
        payload = {'pair': product}
        now = datetime.utcnow()
        r = requests.post(self.api_url + '/0/public/Ticker', data=payload, timeout=settings.API_TIMEOUT)
        data = loads(r.text)
        if 'result' in data:
            data = self.normalize_ticker(data["result"][product])
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
