#!/bin/sh

if ps -ef | grep -v grep | grep twitter_scraper.py ; then
        exit 0
else
        
        python /home/cusp/pbk236/twitter_geo_scraper/twitter_scraper.py &
        exit 0
fi