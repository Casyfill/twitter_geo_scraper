import luigi
from luigi.contrib.s3 import S3Client, S3Target
from os.path import dirname, join, abspath, basename, expandvars
from datetime import datetime
from glob import glob
import os
CREDS_PATH = join(dirname(__file__), '..', '..', 'credentials.json')


class send_file_to_S3(luigi.Task):
    path = luigi.Parameter()
    client = S3Client()
    s3_base = 'qctwitterarchive/current/'

    def output(self):
        s3_path = self.s3_base + basename(self.path)
        return S3Target(path=s3_path, client=self.client)

    def run(self):
        self.client.put(self.path, self.output().path,
                        headers={'Content-Type': 'application/x-sqlite3'})


class send_all_db_to_S3(luigi.Task):
    data_folder = expandvars(os.getenv('TWITTERDATAPATH'))
    log_folder = expandvars(os.getenv('TWITTERLOGS'))
    all_files = glob(data_folder + '/*.db')

    def requires(self):
        return [send_file_to_S3(path=p) for p in self.all_files]

    def output(self):
        return luigi.LocalTarget(join(self.log_folder, datetime.now().strftime('%Y-%m-%d_%H_%M.log')))

    def run(self):
        with self.output().open('r') as f:
            f.write('all data moved to s3')


if __name__ == '__main__':
    luigi.run(main_task_cls=send_all_db_to_S3, local_scheduler=True)
