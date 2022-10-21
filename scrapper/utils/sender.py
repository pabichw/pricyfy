'''sender module'''
from enum import Enum
import smtplib
import os
from email.mime.text import MIMEText


class EmailTemplates(Enum):
    TEST = 0
    PRICE_CHANGE = 1
    WATCH_STARTED = 2


class Sender:
    '''Sender'''
    @staticmethod
    def compose_mail(variables, type):
        '''compose mail'''

        msg = {}
        msg['From'] = os.environ.get("SMTP_FROM")

        if type is EmailTemplates.TEST:
            msg = MIMEText(
                f"""⚠️ TEST ⚠️\nęśąćż\nLorem ipsum doret emet? Emet!""")
            msg['Subject'] = f"""Email service testing"""
        elif type is EmailTemplates.PRICE_CHANGE:
            msg = MIMEText(f"""Price of {variables.get('prod_title', None)} has just went down to 
                            {str(variables.get('price', None))}\n\nThere is a direct link: {variables.get('url', None)}\n\nLast price: {str(variables.get('last_price', None))}""")
            msg['Subject'] = f"""Subject: 💹 Price of {variables.get('prod_title', None)}  went down!"""
        elif type is EmailTemplates.WATCH_STARTED:
            msg = MIMEText(
                f"""Watching offer {variables.get('url', None)} has started. You will be notified once the price has changed!\n\nInitial price: {variables.get('threshold_price', None)}""")
            msg['Subject'] = f"""Subject: ℹ️ Watching has started!"""
        else:
            msg = MIMEText(
                """Unrecognized email template. Please notify development team""")

        return msg.as_string()

    @staticmethod
    def send_mail(
            variables={},
            to=[],
            type=EmailTemplates.PRICE_CHANGE):
        '''send mail'''
        server = smtplib.SMTP(os.environ.get("SMTP_HOST"), 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(os.environ.get("SMTP_FROM"),
                     os.environ.get("SMTP_PASS"))

        server.sendmail(
            os.environ.get("SMTP_FROM"),
            to,
            Sender.compose_mail(
                variables,
                type
            ))
        server.quit()
