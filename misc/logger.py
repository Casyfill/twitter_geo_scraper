#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
from glob import glob
import os
from pathlib import Path

LOGS = Path(os.getenv('TWITTERLOGS', '.'))

def getLogger(recent=False, level=logging.INFO):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    logger.handlers = []
    logger.propagate = False

    filepath = str( LOGS / f'{datetime.datetime.now():%Y-%m-%d}_scraping.log')
    handler = logging.FileHandler( filepath )
    handler.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def mostRecentFile(path, tp='.log'):
    '''returns most recent file in folder'''

    def reduceRecent(current, newPath):
        d = os.stat(newPath).st_ctime

        if d > current[1]:
            return (newPath, d)
        else:
            return current

    path, time = reduce(reduceRecent, glob('*{0}'.format(tp)), (None, 0))
    return path
