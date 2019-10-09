import luigi
from datetime import date
from ..twitter_scraper import config, _get_psql_connection
from ..misc.logger import getLogger
from ..misc.mailer import send_message
# import yaml

class Alert(luigi.Task):
    date = luigi.DateParameter(default=date.today())
    database = config['database']['database']
    treshold = 100

    def _count_tweets(self, con):
        Q = f'''SELECT COUNT(*) FROM tweets
        WHERE (TIMESTAMP 'epoch' + timestamp * INTERVAL '1 second') BETWEEN '{self.date:%Y-%m-%d} 00:00:00' AND '{self.date:%Y-%m-%d} 23:59:59';
        '''

        return con.execute(Q).fetchone()[0]
    
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

        logger = getLogger()

        if count < self.treshold:
            self.alert(count)

        logger.info(f'Got {count} tweets stored for {self.date}')



