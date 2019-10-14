#!/bin/sh

pkill -u pbk236 -f "twitter_geo_scraper/twitter" || echo "Scraper was not running."

echo "restarting twitter scraper"
python /home/cusp/pbk236/twitter_geo_scraper/twitter_scraper.py &
exit 0