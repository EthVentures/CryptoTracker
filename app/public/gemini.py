#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:29:13 2017

@authors: avelkoski
         dconroy
"""

from json import loads
from datetime import datetime
import settings
import logging
import requests
import utils

class Gemini_Market(object):
    """Gemini Market Data"""
    def __init__(self):
        self.api_url = settings.GEMINI_API_URL
        self.exchange = "gemini"
        self.books = ['asks','bids']
        self.products = {'ETHUSD':'eth.gemini.ticker'}
        if settings.GEMINI_API_URL[-1] == "/":
            self.api_url = settings.GEMINI_API_URL[:-1]

    def clean_ticker(self,data):
        clean_data = dict()
        clean_data["ask"] = float(data["ask"])
        clean_data["bid"] = float(data["bid"])
        clean_data["price"] = float(data["last"])
        return clean_data

    def get_ticker(self,product):
        """Get current tick"""
        data = dict()
        now = datetime.utcnow()
        r = requests.get(self.api_url + '/pubticker/' + product)
        data = loads(r.text)
        if 'last' in data:
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
