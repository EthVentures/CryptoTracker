#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:29:13 2017

@authors: avelkoski
         dconroy
"""
from elasticsearch import Elasticsearch, helpers
import os
import sys
import traceback
import logging
import time

def generate_nonce():
    return int(time.time()*10)

def create_indices(es,index_array):
        for index in index_array:
            try:
                if (es.indices.exists(index)):
                    logging.info('Already Exists, Skipping:! ' + index)
                else:
                    es.indices.create(index)
            except Exception as e:
                logging.info(e)
