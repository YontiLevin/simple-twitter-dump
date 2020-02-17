from datetime import datetime
from std.DumperClass import Dumper
from dynaconf import settings


def user_inputs():
    import argparse
    from argparse import RawTextHelpFormatter

    parser = argparse.ArgumentParser(description='Scrape Twitter Easily', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-l', '--lang', dest='language', default=settings.LANGUAGE, help='filter results by language code')
    parser.add_argument('-s', '--sleep', dest='sleep_duration', default=settings.SLEEP_DURATION, help='waiting time between api requests')
    parser.add_argument('-p', '--path', dest='path2results', default=settings.PATH2RESULTS, help='path to results folder')
    parser.add_argument('-m', '--method', dest='method', default=settings.SCRAPING_METHOD,
                        help="""which scraping method to run?\n\t1 - single day\n\t2 - many_days\nenter the number!""")
    parser.add_argument('-n', dest='n', default=settings.SCRAPE_N_DAYS_BACK, help='how many days back to scrape')
    parser.add_argument('-d', '--date', dest='date2scrape', default=settings.DATE2SCRAPE,
                        help='the date you want to scrape')
    parser.add_argument('-q', '--query', dest='query', default=settings.QUERY, help='the search query')
    parser.add_argument('-f', '--file_prefix', dest='csv_prefix', default=settings.CSV_PREFIX, help='csv file prefix')

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    inputs = user_inputs()
    dumper = Dumper(settings, inputs)
    
    if inputs.method == '1':
        dumper.scrape_date(inputs.date2scrape)
    else:
        dumper.scrape_n_days(n=int(inputs.n), end_date=inputs.date2scrape)