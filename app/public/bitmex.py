#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from json import loads
from datetime import datetime
import settings
import logging
import requests
import utils

class BitMex_Market(object):
    """BitMex Market Data"""
    def __init__(self):
        self.api_url = settings.BITMEX_API_URL
        self.exchange = 'bitmex'
        self.products = {'XBTUSD':'btc.bitmex.ticker'}
        if settings.BITMEX_API_URL[-1] == "/":
            self.api_url = settings.BITMEX_API_URL[:-1]

    def normalize_ticker(self,data):
        clean_data = dict()
        clean_data["ask"] = float(data['askPrice'])
        clean_data["bid"] = float(data['bidPrice'])
        clean_data["price"] = float(data['lastPrice'])
        clean_data["volume"] = float(data['volume'])

        return clean_data

    def get_ticker(self, product):
        """Get current tick"""
        now = datetime.utcnow()
        r = requests.get(self.api_url + '/instrument?symbol=' + product, timeout=settings.API_TIMEOUT)
        data = loads(r.text)[0]
        if 'lastPrice' in data:
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
