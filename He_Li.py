import requests
import json

total_reposts = 0
def save_repost(data, level):
    global total_reposts
    total_reposts += 1
    print('{}: {} - {}'.format(total_reposts, level, data['text']))

def get_repost(post_id, page):
    url = 'https://m.weibo.cn/api/statuses/repostTimeline?id={}&page={}'.format(post_id, page)
    resp = requests.get(url)
    resp_json = json.loads(resp.text)
    return resp_json

def get_all_reposts_for(post_id, page, level):
    repost_data = get_repost(post_id, page)
    if repost_data['ok'] == 0:
        return
    reposts_list = repost_data['data']['data']
    for repost in reposts_list:
        save_repost(repost, level)
        if repost['reposts_count']:
            get_all_reposts_for(repost['id'], 1, level + 1) #why 1, not page here? only posts on page 1 are examined?
    get_all_reposts_for(post_id, page + 1, level)

if __name__ == '__main__':
    get_all_reposts_for('4247965625405438', 1, 1)
    print('total reposts: {}'.format(total_reposts))
