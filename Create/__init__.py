import logging

import azure.functions as func
from airtable import Airtable
import random

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
        if airtable.search('Email', req_body['Email']):
            return func.HttpResponse(f"User with this email already exists")
        else:
            req_body['id'] = create_id()

            req_body['actionPoints'] = 0
            response = airtable.insert(req_body)
            records = requests.get(url=all_records_url, headers=adalo_headers)
            request = requests.put(url=f"{update_url}{len(records.json()['records']) + 17}", headers=adalo_headers,
                                   json={
                                       'id': req_body['id']
                                   })
            return func.HttpResponse(
                f"Hello, {response, request.content}. This HTTP triggered function executed successfully.")


def create_id():
    while True:
        uid = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        try:
            airtable.search('ColumnB', uid)
        except requests.HTTPError:
            return uid
