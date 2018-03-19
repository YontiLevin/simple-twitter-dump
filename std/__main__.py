from datetime import datetime
from std import Dumper


def user_inputs():
    import argparse
    from argparse import RawTextHelpFormatter

    parser = argparse.ArgumentParser(description='Scrape Twitter Easily', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-l', '--lang', dest='lang', default='he', help='filter results by language code')
    parser.add_argument('-s', '--sleep', dest='sleep_duration', default='1', help='waiting time between api requests')
    parser.add_argument('-p', '--path', dest='path2results', default='data', help='path to results folder')
    parser.add_argument('-m', '--method', dest='method', default='1',
                        help="""which scraping method to run?\n\t1 - single day\n\t2 - many_days\nenter the number!""")
    parser.add_argument('-n', dest='n', default='10', help='how many days back to scrape')
    parser.add_argument('-d', '--date', dest='date2scrape', default=None,
                        help='the date you want to scrape')
    parser.add_argument('-q', '--query', dest='query', default=' ', help='the search query')

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    inputs = user_inputs()
    dumper = Dumper()
    dumper.lang = inputs.lang
    dumper.data_path = inputs.path2results
    dumper.query = inputs.query
    dumper.sleep_between_queries = inputs.sleep_duration
    if inputs.method == '1':
        dumper.scrape_date(inputs.date2scrape)
    else:
        dumper.scrape_n_days(n=int(inputs.n), end_date=inputs.date2scrape)