from twitter import Twitter, OAuth, TwitterHTTPError
import os
scraperID='DO2'


def getTwitter():
    OAUTH_TOKEN = os.environ('TWITTERACCESSTOKEN')
    OAUTH_SECRET = os.environ('ACCESSTOKENSECRET')
    CONSUMER_KEY = os.environ('TWITTERCONSUMERKEY')
    CONSUMER_SECRET = os.environ('TWITTERCONSUMERSECRET')

    return Twitter(
        auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))



