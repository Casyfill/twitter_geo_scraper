from twitter import Twitter, OAuth, TwitterHTTPError
# import os



def getTwitter(config):
    OAUTH_TOKEN = config['TWITTERACCESSTOKEN']
    OAUTH_SECRET = config['ACCESSTOKENSECRET']
    CONSUMER_KEY = config['TWITTERCONSUMERKEY']
    CONSUMER_SECRET = config['TWITTERCONSUMERSECRET']

    return Twitter(
        auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))



