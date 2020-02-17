from tweepy import OAuthHandler, API, RateLimitError


def twitter_api(settings):
    settings.setenv('secret')
    auth = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

    api = API(auth)
    return api


def RateLimitErrorExecption():
    return RateLimitError


