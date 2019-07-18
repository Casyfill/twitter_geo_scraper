import luigi
from luigi.contrib.s3 import S3Client, S3Target
# from os.path import dirname, join, basename
from pathlib import Path
from datetime import datetime, time
from glob import glob
import pandas as pd
import psycopg2
from luigi.tools.range import RangeMonthly
# CREDS_PATH = join(dirname(__file__), '..', '..', 'credentials.json')

class DOClient(S3Client):

	def __init__(self):
		super().__init__(aws_access_key_id='S77RF4XVGAPRMY4B6QV2',
					     aws_secret_access_key ='bxHXhKRkRPBDgkCYP8PXlEz7YdS63lRFKo/VIXSOpNQ',
					     region_name='nyc3',
					     endpoint_url='https://nyc3.digitaloceanspaces.com')

class Dump_month_to_s3(luigi.Task):
	client = DOClient()
	month = luigi.MonthParameter(default=datetime(2014,1,1))
	v = luigi.NumericalParameter(
        default=0.1, var_type=float, min_value=0, max_value=100
    )

	s3_base = 's3://qctwitterarchive/postgresql_dump/{v}/{date:%Y/%m}.csv'
	pgscon = psycopg2.connect(
		host='localhost',
		database='twitter',
		user='root',
		password='newyork04'
	)
		
	Q = '''SELECT id, user_id, timestamp, lat, lon, application, ct FROM geotweets
		WHERE timestamp >= {S} AND timestamp < {E};
		'''

	@property
	def period(self):
		A = datetime.combine(self.month, time.min).timestamp()
		B = datetime.combine(luigi.MonthParameter().next_in_enumeration(self.month), time.min).timestamp()
		return A, B

	def _get_data(self):
		Q = self.Q.format(S=self.period[0], E=self.period[1])
		return pd.read_sql(Q, self.pgscon)

	def output(self):
		s3_path = self.s3_base.format(date=self.month, v=self.v)
		return S3Target(path=s3_path, client=self.client)

	def run(self):
		data = self._get_data()
		print(f'uploading {len(data)} rows for {self.month}')
		self._upload_csv(data, self.output().path)

	def _upload_csv(self, df, path):
		content = df.to_csv(float_format="%.3f", index=None)
		self.client.put_string(content=content, destination_s3_path=path,
							   ContentType="text/csv")



class Bulk_dump_s3(RangeMonthly):

	v = luigi.NumericalParameter(
        default=0.1, var_type=float, min_value=0, max_value=100
    )

	of = Dump_month_to_s3
	of_params = {'v':v}
	start = luigi.MonthParameter(default=datetime(2014,1,1))
	months_back = luigi.IntParameter(default=60)

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
