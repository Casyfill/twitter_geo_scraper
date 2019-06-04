import luigi
from luigi.contrib.s3 import S3Client, S3Target
# from os.path import dirname, join, basename
from pathlib import Path
from datetime import datetime
from glob import glob
import pandas as pd
import psycopg2
# CREDS_PATH = join(dirname(__file__), '..', '..', 'credentials.json')


class Dump_month_to_s3(luigi.Task):
	client = S3Client()
	month = luigi.DateIntervalParameter('2015-01')
	v = luigi.NumericalParameter(
        default=0.1, var_type=float, min_value=0, max_value=100
    )

	self.s3_base.format = 'https://qctwitterarchive.nyc3.digitaloceanspaces.com/postgresql_dump/{v}/{date:%Y/%m}.csv'
	pgscon = psycopg2.connect(
		host='localhost',
		database='tweets',
		user='root',
		password='newyork04'
	)
		
	Q = '''SELECT id, user_id, timestamp, lat, lon, application, ct FROM tweets
		WHERE timestamp BETWEEN '{S:%Y-%m-%d} 00:00:00' AND '{E:%Y-%m-%d} 00:00:00';
		'''

	@property
	def period(self):
		return self.month.date_a.timestamp(), self.month.date_b.timestamp()

	def _get_data(self):
		Q = self.Q.format(*self.period)
		return pd.read_sql(Q, self.pgscon)

	def  output(self):
		s3_path =  self.s3_base.format(date=self.period.date_a, v=self.v)
		return S3Target(path=s3_path, client=self.client)

	def run(self):
		data = self._get_data()
		print(f'uploading {len(data)} rows for {self.period}')
		self._upload_csv(data, self.output().path)

	def _upload_csv(self, df, path):
		content = df.to_csv(float_format="%.3f", index=None)
        self.client.put_string(
            content=content, destination_s3_path=path, ContentType="text/csv"
        )



# class send_file_to_S3(luigi.Task):
#     path = luigi.Parameter()
# 	client = S3Client()

#     def  output(self):
# 		s3_path =  self.s3_base + basename(self.path)
# 		return S3Target(path=s3_path, client=self.client)

#     def run(self):
# 		self.client.put(self.path, self.output().path,
# 						headers={'Content-Type':'application/x-sqlite3'})


# class send_all_db_to_S3(luigi.Task):
# 	data_folder = os.getenv('TWITTERDATAPATH')
# 	log_folder = os.getenv('TWITTERLOGS')
# 	all_files = glob(data_folder + '/*.db')

# 	def requires(self):
# 		return [send_file_to_S3(path=p) for p in self.all_files]

# 	def output(self):
# 		return luigi.LocalTarget(join(self.log_folder, datetime.now().strftime('%Y-%m-%d_%H_%M.log')))

# 	def run(self)
# 		with self.output().open('r') as f:
# 			f.write('all data moved to s3')


# if __name__ == '__main__':
#     luigi.run(main_task_cls=send_all_db_to_S3, local_scheduler=True)
