#go to m.weibo.cn/searchs

import requests
import json
import sqlite3
import time
import datetime
from datetime import date
from datetime import timedelta

conn = sqlite3.connect('weibo_PSA.sqlite') #generate a database to save relevant info of all the retrieved posts
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS weibo_miaopu(post_id INTEGER, depth INTEGER, retweeted_id INTEGER, 
            user_id INTEGER, screen_name TEXT, verification TEXT, followers_count INTEGER, 
            text TEXT, reposts_count INTEGER, created_at TEXT, original_post_created TEXT, time_difference,
            PRIMARY KEY(post_id,retweeted_id))''') #weibo_miaopu should be replaced by a new name for each original post


total_reposts = 0
def save_repost(data, depth): #depth of a node is the number of edges from the original node to it
    global total_reposts
    total_reposts += 1
    post_id = data['id']
    user_id = data['user']['id']
    screen_name = data['user']['screen_name']
    verification = data['user']['verified']
    followers_count = data['user']['followers_count']
    text = data['text']
    reposts_count = data['reposts_count']
    created_at = data['created_at']
    original_post_created = data['retweeted_status']['created_at']
    time_difference = get_time_difference(created_at,original_post_created)
    if depth == 1:
        retweeted_id = data['retweeted_status']['id']
    else:
        retweeted_id = data['pid']
    try:
        cur.execute('''INSERT INTO weibo_miaopu(post_id, depth, retweeted_id, user_id, screen_name, verification, 
                    followers_count, text, reposts_count, created_at,original_post_created, time_difference) 
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (post_id, depth, retweeted_id, user_id, screen_name, verification, followers_count, text, reposts_count,
                     created_at,original_post_created, time_difference))
        conn.commit()
    except:
        print('duplicate record')
    print('{}: {} - {}'.format(total_reposts, depth, data['text']))

def get_time_difference(created_at,original_post_created):
    start_time = datetime.datetime.strptime(original_post_created, '%a %b %d %H:%M:%S %z %Y').date()

    if '小时前' in created_at:
        end_time = datetime.date.today()
    elif '分钟前' in created_at:
        end_time = datetime.date.today()
    elif '刚刚' in created_at:
        end_time = datetime.date.today()
    elif '昨天' in created_at:
        end_time = datetime.date.today()-timedelta(hours=24)
    else:
        end_time = '{}-{}-{}'.format(2018, created_at.split('-')[0], created_at.split('-')[1]) #may become a problem for some posts
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d').date()
    return (end_time - start_time).days



def get_repost(post_id, page):
    url = 'https://m.weibo.cn/api/statuses/repostTimeline?id={}&page={}'.format(post_id, page)
    resp = requests.get(url)
    resp_json = json.loads(resp.text)
    return resp_json

def get_all_reposts_for(post_id, page, depth):
    repost_data = get_repost(post_id, page)
    if repost_data['ok'] == 0:
        return
    reposts_list = repost_data['data']['data']
    for repost in reposts_list:
        save_repost(repost, depth)
        if repost['reposts_count']:
            get_all_reposts_for(repost['id'], 1, depth + 1) #why 1 not page?
    get_all_reposts_for(post_id, page + 1, depth)

if __name__ == '__main__':
    get_all_reposts_for('4251154122678695', 1, 1)
    print('total reposts: {}'.format(total_reposts))

#4247965625405438
#4251522827316959
#4251154122678695 苗圃公益微博

#how to remove duplicate records with the same post_id, depth, and retweeted_id?