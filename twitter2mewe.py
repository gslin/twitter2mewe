#!/usr/bin/env python3

import configparser
import html
import os
import requests
import sqlite3
import time
import twitter
import urllib

class Twitter2Mewe(object):
    def __init__(self):
        pass

    def start(self):
        home = os.environ['HOME']
        f_conf = '{}/.config/twitter2mewe/config.ini'.format(home)
        f_db = '{}/.config/twitter2mewe/entry.sqlite3'.format(home)

        c = configparser.ConfigParser()
        c.read(f_conf)

        t_ak = c['default']['twitter_access_token']
        t_as = c['default']['twitter_access_token_secret']
        t_ck = c['default']['twitter_consumer_key']
        t_cs = c['default']['twitter_consumer_secret']
        t_user = c['default']['twitter_username']
        t = twitter.Api(access_token_key=t_ak, access_token_secret=t_as, consumer_key=t_ck, consumer_secret=t_cs)

        m_token = c['default']['mewe_token']

        s = sqlite3.connect(f_db)

        sql_insert = 'INSERT INTO entry (twitter_id, created_at) VALUES (?, ?);'
        sql_select = 'SELECT COUNT(*) FROM entry WHERE twitter_id = ?;'

        for status in sorted(list(t.GetUserTimeline(screen_name=t_user)), key=lambda x: x.id):
            # Skip if it's retweet.
            if status.retweeted:
                continue

            # Generate "text" with unescape (workaround).
            text = html.unescape(status.text)
            for u in status.urls:
                text = text.replace(u.url, u.expanded_url)

            # Generate "url"
            url = 'https://twitter.com/{}/status/{}'.format(urllib.parse.quote(t_user), urllib.parse.quote(status.id_str))

            c = s.cursor()

            c.execute(sql_select, (status.id_str, ))
            if 0 == c.fetchone()[0]:
                content = '{} # {}'.format(text, url)
                print('* content = {}'.format(content))

                data = {"text": content, "imageIds": [], "existingFileIds": [], "mediaIds": [], "public": True, "closeFriends": False}
                headers = {'Authorization': 'Sgrouples accessToken= ' + m_token}
                res = requests.post('https://mewe.com/api/v2/home/post', headers=headers, json=data)

                print('* type(status) = {}'.format(type(status)))
                print('* status = {}'.format(status))
                print('* type(res) = {}'.format(type(res)))
                print('* res = {}'.format(res))
                if 200 == res.status_code:
                    c.execute(sql_insert, (status.id_str, int(time.time())))
                    s.commit()
                else:
                    s.rollback()

if '__main__' == __name__:
    t = Twitter2Mewe()
    t.start()
