import subprocess
from subprocess import check_output
import signal
import os
from misc import mailer
from misc import logger
from datetime import datetime

# this script runs scraper if it is not working - it is meant to be runned
# from crontab


def findProcess(processId):
    '''mambo jumbo checking if process exists'''
    ps = subprocess.Popen("ps -ef | grep " + processId,
                          shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    return ('python scraper.py' in output)


def killProcess(name):
    '''kill process by name'''
    pid = int(check_output(["pidof", name]).split()[0])
    os.kill(pid, signal.SIGKILL)


def main():
    '''action - checking if process exists,
starting if not, and logging the result anyway'''
    if not findProcess('python scraper.py'):
        date = datetime.now().strftime('%Y_%m_%d')
        print '%s | deploying new scraper\n' % date
        mailer.send_welcoming()
    	subprocess.call('python scraper.py &', shell=True)
    else:
        log = logger.getLogger(recent=True)
        log.info('Checking: scraper is working')
        print 'Checking: scraper is working'


def main2():
    '''restart process no matter what'''
    if findProcess('python scraper.py'):
    	killProcess('python')
    date = datetime.now().strftime('%Y_%m_%d')
    print '%s | deploying new scraper\n' % date
    mailer.send_welcoming()
    subprocess.call('python scraper.py &', shell=True)

if __name__ == '__main__':
    main2()
