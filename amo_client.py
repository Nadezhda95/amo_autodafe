import os
from amocrm_api import AmoOAuthClient  # for oauth
import json


def create_client():
    url = os.environ.get('DOMAIN')

    f = open('json/Token_amo.json')
    token_amo = json.load(f)
    f.close()

    f = open('json/client_ids.json')
    client_ids = json.load(f)
    f.close()

    client = AmoOAuthClient(
        token_amo['access_token'],
        token_amo['refresh_token'],
        url,
        client_ids['client_id'],
        client_ids['client_secret'],
        client_ids['redirect_uri']
        )

    client.update_tokens()

    return client
