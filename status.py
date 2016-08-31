import subprocess
from subprocess import call
#from subprocess import check_output
import signal
import os
#from misc import mailer
from misc import logger
from datetime import datetime
import sys

# this script runs scraper if it is not working - it is meant to be runned
# from crontab

def scraperIsRunning():
    '''checks if scraper is running, and if many are running'''
    #ps = call(['ps', 'ux' | grep "python scraper.py"')
    #print ps
    proc = subprocess.Popen(['ps ux | grep "scraper.py"',], shell=True, stdout=subprocess.PIPE)
    counter = 0
    while True:
        line = proc.stdout.readline()
        if line=='':
            break
        counter+=1
    if counter<3:
	return False
    elif counter==3:
        return True
    else:
        return 'There are few, need to reboot!'


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


def main(key):
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


def reboot():
    '''restart process no matter what'''
    if findProcess('python scraper.py'):
        killProcess('python')
    
    date = datetime.now().strftime('%Y_%m_%d')
    print '%s | deploying new scraper\n' % date
 #   mailer.send_welcoming()
    subprocess.call('python scraper.py &', shell=True)

def main2(key):
    '''restart process no matter what'''
    if key=='reboot':
        reboot()
    elif key=='status':
        print 'Scraper status:{}'.format(scraperIsRunning())
    else:
        raise IOError('key should be in [reboot, status], {0} applied'.format(key))

if __name__ == '__main__':
    if len(sys.argv)>1:
	key = sys.argv[1]
    else:
        key = 'status'
    main2(key)
