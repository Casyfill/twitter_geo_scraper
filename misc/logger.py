#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
from glob import glob
import os

def getLogger(recent = False):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if recent:
        path = mostRecentFile('.', tp='.log')
        handler = logging.FileHandler(path)
    else:
        date = datetime.datetime.now().strftime('%Y_%m_%d')
        handler = logging.FileHandler('%s_scraping.log' % date)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger



def mostRecentFile(path, tp='.log'):
    '''returns most recent .db file in folder'''

    def reduceRecent(current, newPath):
        d = os.stat(newPath).st_ctime
        if d > current[1]:
            return (newPath, d)

    path, time = reduce(reduceRecent, glob('*%s' % tp), (None, 0))
    return path
