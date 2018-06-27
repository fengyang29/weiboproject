import json
import time
import datetime
from datetime import date
from datetime import timedelta


with open('weibo_PSA_1.json', encoding="utf-8") as file:
    data = json.load(file)


total_posts = 0
for info in data:
    total_posts += 1
    start_time = datetime.datetime.strptime(info['original_post_created'], '%a %b %d %H:%M:%S %z %Y').date()
    created_time = info['created_at']
    if '小时前' in created_time:
        end_time = datetime.date.today()
    elif '分钟前'in created_time:
        end_time = datetime.date.today()
    else:
        end_time = '{}-{}-{}' .format(2018,created_time.split('-')[0],created_time.split('-')[1])
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d').date()
    time_difference = (end_time - start_time).days


    print('{}: {} - {} - {}'.format(total_posts, end_time, time_difference, info['text']))

