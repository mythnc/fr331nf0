import configparser
import json
import pprint
import requests


config_file = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file)
app_setting = config['app']
app_id = app_setting['app id']
app_secret = app_setting['app secret']
short_token = app_setting['short token']
long_token = app_setting.get('long token')

host = 'https://graph.facebook.com'
version = 'v2.10'

def get_long_token():
    # TODO: handle long token expired condition
    if long_token is not None:
        return long_token
    path = '/oauth/access_token'
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_token,
    }
    r = requests.get(host + path, params=params)
    result = r.json()
    long_token = result['access_token']
    save_long_token()


def save_long_token():
    # TODO: if long token alreday existed, this will failed
    with open(config_file, 'a') as f:
        f.write('long token = {}'.format(long_token))


def get_posts():
    url = '{}/{}/me/posts'.format(host, version)
    params = {
        'access_token': long_token,
        'fields': 'comments{comments,message},message,created_time,object_id,id',
    }
    r = requests.get(url, params=params)
    # TODO: handle after
    return r.json()


def save_posts(result):
    with open('data.json', 'w') as f:
        json.dump(result, f)


def read_posts():
    with open('data.json') as f:
        return json.load(f)


if __name__ == '__main__':
    #result = get_posts()
    #save_posts(result)
    pass
