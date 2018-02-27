# IMPORTS
from datetime import datetime, timedelta
from .api_setup import twitter_api, RateLimitErrorExecption
from time import sleep
import csv
from tqdm import tqdm


class Dumper(object):
    def __init__(self):
        self._api = twitter_api()
        self._data_path = '../data'
        self._csv_name = None
        self._query = ' '
        self._retweets = False
        self._today = datetime.today().date()
        self._lang = 'he'
        self._cols = ['text', 'tweet_id', 'created_at', 'user_name', 'user_screen_name', 'used_id']

    @property
    def api(self):
        return self._api

    @property
    def data_path(self):
        return self._data_path

    @data_path.setter
    def data_path(self, path):
        self._data_path = path

    @property
    def csv_name(self):
        if self._csv_name is None:
            self.csv_name = self.today.__str__()
        return self._csv_name

    @csv_name.setter
    def csv_name(self, _name):
        if _name is not None and type(_name) == str:
            self._csv_name = _name

    @property
    def query(self):
        q = self._query
        if not self._retweets:
            q += '-filter:retweets'
        return q

    @query.setter
    def query(self, new_query):
        if new_query is not None and type(new_query) == str:
            self._query = new_query
        else:
            print('Invalid query! - must be a string')

    @property
    def today(self):
        return self._today

    # METHODS
    def loop_over_last_n_days(self, n=10):
        if n > 10:
            print('Can Only Scrape Up To 10 Days Back')
        for delta in range(n-1, -2, -1):
            day_to_scrape = self.today - timedelta(delta)
            day_before = self.today - timedelta(delta) - timedelta(1)
            self.scrape_full_day(day_to_scrape, day_before)

    def scrape_full_day(self, day_date, day_before):
        tweets = []
        print(f'Starting to scrape {day_before.__str__()} ...')
        search_iterator = tqdm(self.search_handle(day_date, day_before))
        for full_tweets, current_date in search_iterator:
            search_iterator.set_description(current_date)
            for tweet in full_tweets:
                tweets.append(self.tweet_handler(tweet))

        with open(f'{self.data_path}/{self.csv_name}.csv', 'w') as f:
            dump = csv.writer(f)
            dump.writerow(self._cols)
            dump.writerows(tweets)

    def search_handle(self, max_date, min_date):
        max_id = None
        waiting_counter = 15
        while True:
            try:
                if self._lang:
                    results = self.api.search(q=self.query,
                                              lang=self._lang,
                                              locale=self._lang,
                                              count=100,
                                              show_user=True,
                                              tweet_mode='extended',
                                              result_type='recent',
                                              max_id=max_id,
                                              until=max_date,
                                              since=min_date)
                else:
                    results = self.api.search(q=self.query,
                                              count=100,
                                              show_user=True,
                                              tweet_mode='extended',
                                              result_type='recent',
                                              max_id=max_id,
                                              until=max_date,
                                              since=min_date)

                assert len(results) > 1, 'no more results'
                last_tweet = results[-1]
                current_date = last_tweet.created_at.__str__()
                max_id = last_tweet.id
                yield results, current_date
                waiting_counter = 15

            except RateLimitErrorExecption():
                yield [], f'Reached Rate Limit - {waiting_counter} min to wait...'
                waiting_counter -= 1
                sleep(1 * 60)
            except Exception as e:
                print(e)
                break

    def tweet_handler(self, tweet):
        text_start, text_stop = tweet.display_text_range
        basic_info = {'text': tweet.full_text[text_start:text_stop],
                      'tweet_id': tweet.id,
                      'created_at': tweet.created_at,
                      'user_name': tweet.user.name,
                      'user_screen_name': tweet.user.screen_name,
                      'user_id': tweet.user.id}
        return basic_info.values()




