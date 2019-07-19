start:
	systemctl start twitter_scraper.service;

status:
	systemctl status twitter_scraper.service;

check:
	systemctl is-active twitter_scraper.service;

stop:
	systemctl stop twitter_scraper.service;

list:
	systemctl list-units;

connect:
	ssh root@165.227.118.82