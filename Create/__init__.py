import logging

import azure.functions as func
from airtable import Airtable
import random
import bcrypt

import requests

base_id = "appkzUYKXEL4LGVzf"
table_name = 'offzmi_table'
api_key = 'keyayJEttwX4dBeZv'

airtable = Airtable(base_id, table_name, api_key)
update_url = "https://api.adalo.com/v0/apps/b1610ffb-c5ee-4ec5-9a9e-3daae6af8061/collections/t_555b0678dcbf497fa89f55dbdd94fe21/"
all_records_url = "https://api.adalo.com/v0/apps/b1610ffb-c5ee-4ec5-9a9e-3daae6af8061/collections/t_555b0678dcbf497fa89f55dbdd94fe21"

adalo_headers = {
    "Authorization": "Bearer duwa7prlbaojtqrc9cpiq5j9f"
}


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        # try:
        #     airtable.search('Email', req_body['Email'])
        # except requests.HTTPError:
        req_body['id'] = create_id()
        req_body['salt'], req_body['Password'] = hash_password(req_body['Password'])
        req_body['actionPoints'] = 0
        response = airtable.insert(req_body)
        records = requests.get(url=all_records_url, headers=adalo_headers)
        requests.post(url=f"{update_url}{len(records.json()['records'])}", headers=adalo_headers, json={
            'id': req_body['id']
        })
        return func.HttpResponse(f"Hello, {response}. This HTTP triggered function executed successfully.")
        # else:
        #     return func.HttpResponse(f"User with this email already exists")


def create_id():
    while True:
        uid = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        try:
            airtable.search('ColumnB', uid)
        except requests.HTTPError:
            return uid


def hash_password(password):
    byte_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(byte_password, salt)
    return str(salt)[2:-1], str(hashed_password)[2:-1]
