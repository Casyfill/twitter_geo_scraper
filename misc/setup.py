import sqlite3
import logging
import datetime
from  pathlib import Path
import os

DATAPATH = Path(os.path.expandvars(os.getenv("TWITTERDATAPATH", '.')))

def setup(scraperID, timestamp):
	'''generate database'''
	filename = f'{scraperID}_{timestamp:%Y-%m-%d_%H_%M}.db'
	path = DATAPATH / filename
	try:
		conn = sqlite3.connect(str(path.absolute()))
	except Exception as inst:
		raise Exception(inst, path)
	logging.info(path)

	c = conn.cursor()

	c.execute('CREATE TABLE IF NOT EXISTS tweets (id INTEGER PRIMARY KEY, timestamp INTEGER, lon REAL, lat REAL, tweet TEXT, user_id INTEGER, rtwts INTEGER, fvrts INTEGER, application TEXT, source TEXT, raw TEXT )')
	c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER, timestamp TEXT, raw TEXT, CONSTRAINT pk PRIMARY KEY (id, timestamp))''')
	conn.commit()
	conn.close()
	return  str(path)


if __name__ == '__main__':
	print(DATAPATH)
	x = setup('TEST', datetime.datetime.now())
	print(x)
