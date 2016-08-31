from twitter import Twitter, OAuth, TwitterHTTPError

scraperID='CUSP'


def getTwitter():
    OAUTH_TOKEN =     'OAUTH_TOKEN'
    OAUTH_SECRET =    'OAUTH_SECRET'
    CONSUMER_KEY =    'CONSUMER_KEY'
    CONSUMER_SECRET = 'CONSUMER_SECRET'

    return Twitter(
        auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))



