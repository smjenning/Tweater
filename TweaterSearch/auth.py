import time
from getpass import getpass
from textwrap import TextWrapper
import tweepy

def GetTweepyAPI():
    #obviously this needs some error handling
    CKEY = ''
    CSEC = ''
    key = '-'
    secret = ''
    auth = tweepy.OAuthHandler(CKEY,CSEC)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)
    return api

#does this work without the keys?