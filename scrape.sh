#!/bin/sh

if ps -ef | grep -v grep | grep twitter_scraper.py ; then
        echo "seems to work fine"
        exit 0
else
        
        python /home/cusp/pbk236/twitter_geo_scraper/twitter_scraper.py &
        echo "no scraper working, rebooting!"
        exit 0
fi