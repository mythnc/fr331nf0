import configparser
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
    access_token = result['access_token']
    save_long_token(access_token)
    return access_token


def save_long_token(access_token):
    # TODO: if long token alreday existed, this will failed
    with open(config_file, 'a') as f:
        f.write('long token = {}'.format(access_token))


token = get_long_token()
print(token)
