import logging
import os

import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import requests


sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
from_email = Email("admin@offzmi.com")


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        logging.info(str(req_body))
        requests.post(url='https://hooks.zapier.com/hooks/catch/12437001/baquxp0/', data=req_body['fields']['contactForm_email'])
    except ValueError:
        pass
    else:
        if 'contactForm_email' in req_body['fields']:
            to_email = req_body['fields']['contactForm_email']['value']

            invitation_letter = """
                Вітаємо!\n
                \n
                Це Ваші персональні посилання для завантаження додатку:\n
                https://play.google.com/store/apps/details?id=com.unkd.offzmi\n
                https://apps.apple.com/us/app/off-zmi/id1626418738\n
                
                Будь ласка, перейдіть за посиланням відповідно до Вашої платформи, завантажте додаток та зареєструйтесь.\n
                Ви можете розпочати публікацію новин одразу після авторизації.\n
                \n
                З найкращими побажаннями команда OffЗМІ!\n
                \n
                Нам важливо, що Ви з нами.
            """
            content = Content('text/plain', invitation_letter)
            subject = 'Запрошення до OffЗМІ'
        else:
            to_email = from_email
            subject = "Feedback від користувача!"
            content = Content('text/html', req_body['Feedback'])

        mail = Mail(from_email, To(to_email), subject, content)
        mail_json = mail.get()
        response = sg.client.mail.send.post(request_body=mail_json)
        return func.HttpResponse(f'{str(response.status_code)}, {str(response.headers)}')

