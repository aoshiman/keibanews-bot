# -*- coding: utf-8 -*-

from __future__ import print_function
from time import localtime, mktime, strftime
import email.utils
import feedparser
from twython import Twython, TwythonError
from docopt import docopt
import conf
from setting import FILE, URL


__usage__="""
Usage:
    keibanews-bot.py tweet [--user=<account>] [--no-tweet]

Options:
    -h --help           Show this screen
    --version           Show version
    --user=<account>    tweet user [default: keiba_news]
    --no-tweet          tweet to stdout

"""


def file_open(f):
    try:
        with open(f) as fp:
            return fp.read()
    except:
        pass


def parse_feed(u):
    data = feedparser.parse(u)
    feed = []
    for entry in data.entries:
        feed.append([entry.published, entry.title, entry.link])
    feed.reverse()
    return feed


def tweet_news():
    # OAuth setting
    args = docopt(__usage__)
    config = conf.ParseConf()
    oauth_conf = config.get_items('oauth_conf')
    if args['--user']:
        access_conf = config.get_items(args['--user'])
    twitter = Twython(
    oauth_conf['consumer_key'],
    oauth_conf['consumer_secret'],
    access_conf['access_token'],
    access_conf['access_secret']
    )
    feed = parse_feed(URL)
    latest = file_open(FILE)

    with open(FILE, 'w+') as fp:
        for entry in feed:
            _date, title, url = entry[0], entry[1], entry[2]
            entry_date = strftime('%Y/%m/%d %H:%M',localtime(mktime(email.utils.\
                                                        parsedate(_date))+32400))
            if not latest or entry_date > latest:
                post = u'{0} {1} {2}'.format(entry_date, title, url)
                if args['--no-tweet']:
                    print(post)
                else:
                    try:
                        twitter.update_status(status = post)
                    except TwythonError as e:
                        print(e)
                latest = entry_date
        fp.write(latest)

if __name__ == '__main__':
    tweet_news()
