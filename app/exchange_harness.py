#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from json import loads
from datetime import datetime
import settings
import logging
import requests
import utils
import ccxt
from time import sleep
class ExchangeHarness(object):
    """Poloniex Market Data"""
    def __init__(self,exchange_id):
        self.symbols = ['BTC/USD','ETH/USD']
        self.exchange_id = exchange_id.lower()
        self.products = {'ETH/USD': 'eth.{}.ticker'.format(self.exchange_id),
                         'BTC/USD': 'btc.{}.ticker'.format(self.exchange_id)}
        self.exchange = getattr(ccxt,self.exchange_id)({
        'enableRateLimit': True,  # this option enables the built-in rate limiter
    })
        # self.markets = self.exchange.load_markets()
    def clean_ticker(self,data):
        clean_data = dict()
        now = datetime.utcnow()
        clean_data['tracker_time'] = now
        clean_data["ask"] = float(data["ask"])
        clean_data["bid"] = float(data["bid"])
        clean_data["price"] = float(data["last"])
        clean_data["exchange"] = self.exchange_id
        clean_data["product"] = data['symbol']
        clean_data['info'] = data['info']
        clean_data["size"] = float(data['baseVolume'])
        clean_data["volume"] = float(data['quoteVolume'])
        clean_data['time'] = data['timestamp']
        for k,v in data.items():
            if k not in clean_data.keys():
                clean_data[k]=v
        # if not clean_data["last"]:
        #     clean_data['last'] =
        return clean_data

    def get_ticker(self,symbol):
        ticker = self.exchange.fetch_ticker(symbol)
        clean = self.clean_ticker(ticker)
        return clean

    def record_ticker(self, es):
        """Record current tick"""
        for product in self.products.keys():
            es_body=self.get_ticker(product)
            # print(es_body)
            # if 'price' in es_body:
            try:
                es.create(index=self.products[product], id=utils.generate_nonce(), doc_type='ticker', body=es_body)
            except:
                raise ValueError("Misformed Body for Elastic Search on " + self.exchange_id)

