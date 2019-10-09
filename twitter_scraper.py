# from psycopg2.extras import execute_values
import time
import datetime
# import csv
import json
# import os
import re
import signal
import sys
import time
from pathlib import Path

import pandas as pd
import sqlalchemy as sqa
import yaml

from misc.auth import getTwitter
from misc.logger import getLogger
from misc.setup import setup

# import sqlite3
# Total of 20 seconds sleep between rounds
TIME = 25.

with (Path(__file__).parent / 'config.yaml').open('r') as f:
	config = yaml.safe_load(f)

def getSource(txt):
    sourcer = re.compile('(?:.*>)(.*)(?:<\/a>)')
    x = sourcer.search(txt)
    if x:
        return x.groups()[0]
    else:
        return 'unknnown'


def _get_psql_connection(user=None, password=None, host='localhost', port='5432', database='twitter'):
    if user is None or password is None:
        con_string = f'postgresql+psycopg2:///{database}'
    else:
        con_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    engine = sqa.create_engine(con_string, client_encoding='utf8')
    
    return engine.connect()


def main():
    '''main process'''
    logger = getLogger()
    ts = datetime.datetime.now()
    logger.info(f'{ts:%Y_%m_%d}: start logging')
    # create DB if does not exist


    #ID = setup('DO2', ts)

    # Connect to DB
    logger.info('Connecting to postgress')

    conn = _get_psql_connection(**config['database'])


    def signal_handler(signal, frame):
        # Close connection on interrupt
        conn.close()
        sys.stdout.flush()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    logger.info('Getting twitter connection')
    twitter = getTwitter(config['twitter'])

    nodes = [
        # {'geocode': '40.783288,-73.967090,7mi', 'since': '0'},
        # {'geocode': '40.729992,-73.993841,7mi', 'since': '0'},
        # {'geocode': '40.830778,-73.942806,7mi', 'since': '0'}
        {'geocode': '40.830956,-73.910179,7mi', 'since': '0'},
        {'geocode': '40.663972,-73.956871,8mi', 'since': '0'},
        {'geocode': '40.688708,-73.779544,8mi', 'since': '0'},
        {'geocode': '40.580584,-74.152908,9mi', 'since': '0'}
    ]

    
    sleepTime = TIME / len(nodes)
    # today = datetime.datetime.today()

    while True:
        logger.info('cycle: getting tweets...')
        print('cycle: getting tweets...')
        for node in nodes:
            # fExecute Query
            try:
                t = twitter.search.tweets(geocode=node['geocode'],
                                          result_type='recent',
                                          count=100, since_id=node['since'])
            except Exception as e:
                logger.info('Error getting tweet: %s' % e)
                # Could be twitter is overloaded, sleep for a minute before
                # starting again
                time.sleep(60)
                continue

            # Go through the results and create arrays to add to DB
            tweets = []
            users = []
            # logger.info('Collecting geotagged tweets')
            for status in t['statuses']:
                if status['geo'] is not None:

                    user = status['user']
                    del status['user']

                    timestamp = int(datetime.datetime.strptime(
                        status['created_at'],
                        '%a %b %d %H:%M:%S +0000 %Y'
                    ).strftime("%s"))

                    tweets.append({
                        'id':status['id_str'],
                        'timestamp': timestamp,
                        'lon':status['geo']['coordinates'][0],
                        'lat':status['geo']['coordinates'][1],
                        'text':status['text'],
                        'user_id':user['id'],
                        'rtwts':status['retweet_count'],
                        #'fwrts':status['favorite_count'],
                        'application':getSource(status['source']),
                        'raw':json.dumps(status)
                    })
                    users.append({
                        'id':user['id'],
                        'timestamp':timestamp,
                        'raw':json.dumps(user)
                    })

                else:
                    pass

            # Add to DB
            dbs = {
                'tweets' : pd.DataFrame(tweets),
                'users' : pd.DataFrame(users)
            }

            try:
                for name, df in dbs.items():
                    if len(df) > 0:
                        print(f'Writing to {name}: {len(df)}')
                        df.to_sql(name, con=conn, if_exists='append')
                    else:
                        print(f'No data in {name}')
                conn.commit()

                node['since'] = t['search_metadata']['max_id_str']


            except Exception as e:
                logger.info(f'Failed saving tweets, reconnecting')
                logger.info(str(e))
                time.sleep(60)
                conn = _get_psql_connection(**config['database'])

            # Sleep between nodes
            # logger.info('sleep for %f' % sleepTime)
            time.sleep(sleepTime)

        sys.stdout.flush()

if __name__ == '__main__':
    main()
