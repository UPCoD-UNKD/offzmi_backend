import logging

import bcrypt
from requests import HTTPError

import azure.functions as func
from airtable import Airtable


base_id = "appkzUYKXEL4LGVzf"
table_name = 'offzmi_table'
api_key = 'keyayJEttwX4dBeZv'

airtable = Airtable(base_id, table_name, api_key)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        res = airtable.search('Email', req_body['Email'])
        try:
            if len(res) == 0 or res[0]['fields']['Password'] != check_password(res[0]['fields']['salt'], req_body['Password']):
                raise HTTPError
        except HTTPError:
            return func.HttpResponse(f"Wrong email or password")
        else:
            return func.HttpResponse(f"Success")


def check_password(salt, password):
    salt = salt.encode('utf-8')
    byte_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(byte_password, salt)
    return str(hashed_password)[2:-1]
