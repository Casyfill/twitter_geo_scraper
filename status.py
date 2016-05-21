import subprocess
from misc import mailer
# from misc import auth
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


def main():
    '''action - checking if process exists,
starting if not, and logging the result anyway'''
    if not findProcess('scraper.py'):
        date = datetime.now().strftime('%Y_%m_%d')
        print '%s | deploying new scraper\n' % date
        mailer.send_welcoming()
        subprocess.call('python scraper.py &', shell=True)

    else:
        log = logger.getLogger(recent=True)
        log.info('Checking: scraper is working')
        print 'Checking: scraper is working'


if __name__ == '__main__':
    main()
