#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from json import loads
from datetime import datetime
import settings
import logging
import requests
import utils

class BitTrex_Market(object):
    """BitTrex Market Data"""
    def __init__(self):
        self.api_url = settings.BITTREX_API_URL
        self.exchange = 'bittrex'
        self.products = {'USDT-ETH':'eth.bittrex.ticker',
                         'USDT-BTC':'btc.bittrex.ticker'}
        if settings.BITTREX_API_URL[-1] == "/":
            self.api_url = settings.BITTREX_API_URL[:-1]

    def clean_ticker(self,data):
        clean_data = dict()
        clean_data["ask"] = float(data["Ask"])
        clean_data["bid"] = float(data["Bid"])
        clean_data["price"] = float(data["Last"])
        return clean_data

    def get_ticker(self,product):
        """Get current tick"""
        payload = {'market': product}
        now = datetime.utcnow()
        r = requests.post(self.api_url + '/v1.1/public/getticker', data=payload, timeout=settings.API_TIMEOUT)
        data = loads(r.text)
        if 'result' in data:
            data = self.clean_ticker(data["result"])
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
