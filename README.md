Scraper for twitter streaming data, set up to collect geolocated tweets within NYC.

in order to start data collection:

1. Be sure to have twitter python library installed
2. Set up AUTH in misc.auth.py;
3. run ./reboot_twitter.sh : it will create new screen, and run twitter scraping within this screen. every time you run the script, screen is terminated and, then, rebooted.
4. [optional] - deploy crontab.txt as cronjob (crnotab crontab.txt). Feel free to replace emails and reboot frequency.
