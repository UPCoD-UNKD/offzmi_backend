import azure.functions as func
import requests

all_records_url = "https://api.adalo.com/v0/apps/b1610ffb-c5ee-4ec5-9a9e-3daae6af8061/collections/t_555b0678dcbf497fa89f55dbdd94fe21"
update_url = "https://api.adalo.com/v0/apps/b1610ffb-c5ee-4ec5-9a9e-3daae6af8061/collections/t_555b0678dcbf497fa89f55dbdd94fe21/"

adalo_headers = {
    "Authorization": "Bearer duwa7prlbaojtqrc9cpiq5j9f"
}


def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        records = requests.get(url=all_records_url, headers=adalo_headers)
        for i, obj in enumerate(records.json()['records']):
            if str(obj['id']) == req_body['id']:
                r = requests.put(
                                    url=f"{update_url}{obj['Element Id']}", headers=adalo_headers,
                                    json={'Action points': obj['Action points'] + 1}
                                )
                return func.HttpResponse(str(r.content))
        return func.HttpResponse('Your invite id in not valid')
