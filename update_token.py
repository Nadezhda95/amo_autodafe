import requests
import json
import os
import time

f = open('json/Token_amo.json')
token_amo = json.load(f)
f.close()


def update_token_amo(token_json):
    domain = os.environ.get('DOMAIN')
    url = 'https://' + domain + '/oauth2/access_token'

    f = open('json/client_ids.json')
    client_ids = json.load(f)
    f.close()

    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        'client_id': client_ids['client_id'],
        'client_secret': client_ids['client_secret'],
        'grant_type': client_ids['grant_type'],
        'refresh_token': token_json['refresh_token'],
        'redirect_uri': client_ids['redirect_uri']
    }

    response = requests.post(url=url, json=body, headers=headers)

    f = open('json/Token_amo.json', 'w')
    f.write(response.text)
    f.close()


while True:
    update_token_amo(token_amo)
    time.sleep(token_amo['expires_in'])
