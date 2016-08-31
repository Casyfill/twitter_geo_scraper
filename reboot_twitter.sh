#!/bin/sh

# Kill 1
screen -X -S tscraper quit

# Kill 2
killall twitter_scraper

# Change directory  
cd /green-projects/project-qc_soc_media/workspace/share/twitter_geo_scraper

# Start the server again 
screen -S tscraper -d -m ./launch_scraper.sh
echo "scraper rebooted!"
