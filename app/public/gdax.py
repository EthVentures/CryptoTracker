#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:29:13 2017

@authors: avelkoski
         dconroy
"""

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
        self.exchange = "gdax"
        self.products = {'ETH-USD': 'eth.gdax.ticker'}
        self.books = ['asks', 'bids']
        if settings.GDAX_API_URL[-1] == "/":
            self.api_url = settings.GDAX_API_URL[:-1]

    def clean_ticker(self, data):
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
        r = requests.get(self.api_url + '/products/' + product + '/ticker')
        data = loads(r.text)
        if 'price' in data:
            data = self.clean_ticker(data)
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

    def clean_candle(self, data, product):
        """Record current tick"""
        clean_data = dict()
        clean_data['timestamp']= datetime.strftime(datetime.utcfromtimestamp(data[0]),'%Y-%m-%dT%H:%M:%S.%fZ')
        clean_data['low']= float(data[1])
        clean_data['high']= float(data[2])
        clean_data['open']= float(data[3])
        clean_data['close']=float(data[4])
        clean_data['volume']=float(data[5])
        return clean_data

    def get_candle(self, product, period):
        """Get candles"""
        data = dict()
        now  = datetime.utcnow()
        start = (now - timedelta(seconds=int(period)))
        payload = {'start': start,
                   'end': now,
                   'granularity': period, }

        r = requests.get(self.api_url + '/products/' + product + '/candles', data=payload)
        data=loads(r.text)
        data = self.clean_candle(data[0], product)
        data["tracker_time"] = now
        data["product"] = product
        data["period"] = period
        data["exchange"] = self.exchange
        return data

    def record_candle(self, es, period):
        """Record candle"""
        for product in self.products:
            es.create(index='eth.gdax.candle', id=utils.generate_nonce(), doc_type='ticker', body=self.get_candle(product, period))
