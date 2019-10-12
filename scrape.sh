#!/bin/sh

if ps -ef | grep -v grep | grep twitter_scraper.py ; then
    echo "rebooting twitter scraper"
    pkill -u pbk236 -f "twitter_geo_scraper"
    python /home/cusp/pbk236/twitter_geo_scraper/twitter_scraper.py
    echo "xoxoxo"
    exit 0
else
    echo "no scraper working, rebooting!" &
    python /home/cusp/pbk236/twitter_geo_scraper/twitter_scraper.py &
    exit 0
fi
      