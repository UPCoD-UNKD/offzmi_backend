import logging

import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content


sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
from_email = Email("admin@offzmi.com")
to_email = "admin@offzmi.com"
subject = "Feedback від користувача!"


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        content = Content('text/html', req_body['Feedback'])
        mail = Mail(from_email, To(to_email), subject, content)
        mail_json = mail.get()
        response = sg.client.mail.send.post(request_body=mail_json)
        return func.HttpResponse(f'{response.status_code}, {response.headers}')
