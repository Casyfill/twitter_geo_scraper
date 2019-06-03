import os
import sqlite3
from datetime import date, datetime
from glob import glob
from pathlib import Path

import luigi
# import pandas as pd
from luigi.contrib.postgres import CopyToTable, PostgresTarget

DATA_PATH = '/root/data_dumps'

class SQLite_to_Postgres(CopyToTable):

    sqlite_path = luigi.Parameter(default='~/data_dumps/DO2_2018-03-12_17_20.db')
    
    host='localhost'
    database='twitter'
    user='root'
    password='newyork04'
    table='tweets'
    columns= ['id', 'timestamp', 'lon', 'lat',
             'text', 'user_id',
             'rtwts', 'fvrts', 'application',
             'raw' ]

    SQQ = '''SELECT id, timestamp, lon, lat,
                    tweet as text, user_id,
                    rtwts, fvrts, application,
                    raw FROM tweets;
    '''

    def _sqlite_connect(self):
        try:
            conn = sqlite3.connect(self.sqlite_path)
        except Exception as e:
            raise ValueError(f'Failed to access sqlite: {e}')
        return conn

    def rows(self):
        sqc = self._sqlite_connect()
        
        try:
            data = sqc.execute(self.SQQ).fetchall()
        except sqlite3.OperationalError:
            data = []  # empty file

        print(f'Writing {len(data)} rows to Postgres')
        return data


class BulkSQLite(luigi.Task):

    mindate = luigi.DateHourParameter(default=datetime(2018,3,2, 0))

    @staticmethod
    def _filter(path, mindate):
        _name = Path(path).name.split('_')[1]
        _date = datetime.strptime(_name, '%Y-%m-%d')
        return _date > mindate

    def _get_paths(self):
        _paths = glob(DATA_PATH + '/*.db')

        return [p for p in _paths if self._filter(p, self.mindate)]
        
    def requires(self):
        paths = self._get_paths()
        return [SQLite_to_Postgres(sqlite_path=path) for path in paths]
