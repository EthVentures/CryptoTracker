#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:29:13 2017

@authors: avelkoski
         dconroy
"""
import elasticsearch
import time
import logging

def generate_nonce():
    return int(time.time()*10)

def create_index(es,index):
        if (es.indices.exists(index)):
            logging.info('Already Exists, Skipping:! ' + index)
        else:
            es.indices.create(index)
