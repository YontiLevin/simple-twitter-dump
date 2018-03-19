# IMPORTS
from datetime import datetime, timedelta
from std.api_setup import twitter_api, RateLimitErrorExecption
from time import sleep
import csv
from tqdm import tqdm
import os
from sys import exit


class Dumper(object):
    def __init__(self):
        self._api = twitter_api()
        self._data_path = 'data'
        self._csv_name = 'twitter_dump'
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
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, new_lang):
        self._lang = new_lang

    @property
    def today(self):
        return self._today

    # METHODS
    def scrape_last_n_days(self, n=10):
        if n > 10:
            print('Can Only Scrape Up To 10 Days Back')
        for delta in range(n, -1, -1):
            day_to_scrape = self.today - timedelta(delta)
            self.scrape_date(day_to_scrape)

    def scrape_date(self, date_2_scrape):
        if type(date_2_scrape) is str:
            try:
                date_2_scrape = datetime.strptime(date_2_scrape, '%Y-%m-%d').date()
            except:
                print('Bad Date Format\nPlease enter Y-M-D\ni.e, 2018-03-15')
                exit(1)
        next_day = date_2_scrape + timedelta(1)
        tweets = []
        print(f'Starting to scrape {date_2_scrape.__str__()} ...')
        search_iterator = tqdm(self.search_handle(date_2_scrape, next_day))
        for full_tweets, current_date in search_iterator:
            search_iterator.set_description(current_date)
            for tweet in full_tweets:
                tweets.append(self.tweet_handler(tweet))

        self.dump2csv(tweets, date_2_scrape)

    def search_handle(self, min_date, max_date):
        max_id = None
        waiting_counter = 15
        while True:
            try:
                if self.lang:
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
        return list(basic_info.values())

    def dump2csv(self, tweets, day_before):
        os.makedirs(self.data_path, exist_ok=True)
        file_name = f'{self.data_path}/{self.csv_name}_{day_before.__str__()}.csv'
        if os.path.isfile(file_name):
            existing_tweets = set()
            with open(file_name, 'r') as f:
                old_csv = csv.reader(f)
                next(old_csv)
                for _, tweet_id, *other in old_csv:
                    existing_tweets.add(int(tweet_id))

            tweets = [tweet for tweet in tweets if tweet[1] not in existing_tweets]
            with open(file_name, 'a') as f:
                old_csv = csv.writer(f)
                old_csv.writerows(tweets)
            print(f'{file_name} already existed')
            print(f'#tweets before = {len(existing_tweets)}')
            print(f'#tweets after = {len(existing_tweets)+len(tweets)}\n')
        else:
            with open(file_name, 'w') as f:
                dump = csv.writer(f)
                dump.writerow(self._cols)
                dump.writerows(tweets)
            print(f'Saved as {file_name}')
            print(f'#tweets = {len(tweets)}\n')

if __name__ == '__main__':
    dumper = Dumper()
    dumper.scrape_date('2018-03-15')