import luigi
from luigi.contrib.s3 import S3Client, S3Target
# from os.path import dirname, join, basename
from pathlib import Path
from datetime import datetime, time
from glob import glob
import pandas as pd
from datetime import date
import psycopg2
from luigi.tools.range import RangeMonthly
import yaml

with (Path(__file__).parent / 'credentials.yaml').open('r') as f:
	creds = yaml.safe_load(f)

class DOClient(S3Client):

	def __init__(self):
		super().__init__(endpoint_url='https://nyc3.digitaloceanspaces.com',
						 **creds['spaces'])


class SpaceTask(luigi.Task):
	client = DOClient()

	def _upload_csv(self, df, path):
		content = df.to_csv(float_format="%.3f", index=None)
		self.client.put_string(content=content, 
							   destination_s3_path=path,
							   ContentType="text/csv")


class Dump_month_to_s3(SpaceTask):
	month = luigi.MonthParameter(default=datetime(2014,1,1))
	v = luigi.NumericalParameter(
        default=1.0, var_type=float, min_value=0, max_value=100
    )
	

	s3_base = 's3://qctwitterarchive/postgresql_dump/{v}/{date:%Y/%m}.csv'
	pgscon = psycopg2.connect(
		**creds['database']
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


class Bulk_dump_s3(RangeMonthly):

	v = luigi.NumericalParameter(
        default=0.1, var_type=float, min_value=0, max_value=100
    )

	of = Dump_month_to_s3
	of_params = {'v':1.0}
	start = luigi.MonthParameter(default=datetime(2014,1,1))
	months_back = luigi.IntParameter(default=60)


class GenerateTimeline(SpaceTask):
	
	date = luigi.DateParameter(default=date.today())
	origin = luigi.Parameter(default='DO')
	s3_base = 's3://qctwitterarchive/postgresql_dump/timeline_{origin}_{date:%Y-%m-%d}.csv'
	pgscon = psycopg2.connect(
		**creds['database']
	)
		
	Q = '''SELECT 
		   extract(year from to_timestamp(timestamp)) as yyyy,
		   to_char(to_timestamp(timestamp), 'Mon') as mon,
	       count(*) as tweets
           FROM tweets
		   GROUP by 1, 2
		   ORDER BY yyyy, mon;
		'''

	def output(self):
		s3_path = self.s3_base.format(date=self.date, origin=self.origin)
		return S3Target(path=s3_path, client=self.client)

	def _get_data(self):
		return pd.read_sql(self.Q, self.pgscon)

	def run(self):
		data = self._get_data()
		self._upload_csv(data, self.output().path)


