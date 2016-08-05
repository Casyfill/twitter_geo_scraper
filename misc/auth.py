from twitter import Twitter, OAuth, TwitterHTTPError

scraperID='DO'


mailCredentials = {
'apiKey' : 'key',
'recipients' : ['casyfill@gmail.com'],
'address' : 'address'  
}

def getTwitter():
    OAUTH_TOKEN = 'OAUTH_TOKEN'
    OAUTH_SECRET = 'OAUTH_SECRET'
    CONSUMER_KEY = 'CONSUMER_KEY'
    CONSUMER_SECRET = 'CONSUMER_SECRET'

    return Twitter(
        auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
