from tweepy import OAuthHandler, API, RateLimitError
from .twitter_credentials import *


def twitter_api():
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = API(auth)
    return api


def RateLimitErrorExecption():
    return RateLimitError


