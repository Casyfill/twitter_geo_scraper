#!/bin/sh
echo "$(date) rebooting scraper" >> reboot_logger.txt
python twitter_scraper.py
