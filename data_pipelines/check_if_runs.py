import luigi
from datetime import date
import yaml
from pathlib import Path
from ..misc.logger import getLogger
from ..misc.mailer import send_message
import sqlalchemy as sqa
# import yaml

with (Path(__file__).parent / '..' / 'config.yaml').open('r') as f:
	config = yaml.safe_load(f)

def _get_psql_connection(user=None, password=None, host='localhost', port='5432', database='twitter'):
    if user is None or password is None:
        con_string = f'postgresql+psycopg2:///{database}'
    else:
        con_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    engine = sqa.create_engine(con_string, client_encoding='utf8')
    
    return engine.connect()

class Alert(luigi.Task):
    date = luigi.DateParameter(default=date.today())
    database = config['database']['database']
    treshold = 100

    def _count_tweets(self, con):
        self.query = f'''SELECT COUNT(*) FROM tweets
        WHERE (TIMESTAMP 'epoch' + timestamp * INTERVAL '1 second') BETWEEN '{self.date:%Y-%m-%d} 00:00:00' AND '{self.date:%Y-%m-%d} 23:59:59';
        '''

        return con.execute(self.query).fetchone()[0]
    
    def alert(self, count):
        subject = f'CUSP2 Twitter Scraper Alert: {self.date:%Y-%m-%d}'
        text = f'For {self.date:%Y-%m-%d}, found only {count} tweets!'
        recipients = ['casyfill@gmail.com',]
        send_message(text=text,
                     recipients=recipients, 
                     subject=subject,
                     apiKey=config['mailgun']['apiKey'])

    def run(self):
        con = _get_psql_connection(**config['database'])
        count = self._count_tweets(con)

        logger = getLogger(mode='check')

        if count < self.treshold:
            self.alert(count)
            raise Exception(count, self.query)

        logger.info(f'Got {count} tweets stored for {self.date}')



