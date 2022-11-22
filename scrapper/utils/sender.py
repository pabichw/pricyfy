'''sender module'''
from enum import Enum
import smtplib
import os
from email.mime.text import MIMEText
from utils.calc import get_change


class EmailTemplates(Enum):
    TEST = 0
    PRICE_RAISE = 1
    PRICE_DROP = 2
    WATCH_STARTED = 3
    WATCH_CANCELLED = 4


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
        elif type is EmailTemplates.PRICE_RAISE:
            change = get_change(variables.get('price', 0),
                                variables.get('last_price', 0))

            msg = MIMEText(f"""Price of {variables.get('prod_title', None)} has just raised to 
                            {str(variables.get('price', None))}\n\nThere is a direct link: {variables.get('url', None)}\n\nLast price: {str(variables.get('last_price', None))}\nChange: {round(change, 2)}%""")
            msg['Subject'] = f"""🔺 Price of {variables.get('prod_title', None)} has raised!"""
        elif type is EmailTemplates.PRICE_DROP:
            change = get_change(variables.get('price', 0),
                                variables.get('last_price', 0))

            msg = MIMEText(f"""Price of {variables.get('prod_title', None)} has just went down to 
                            {str(variables.get('price', None))}\n\nThere is a direct link: {variables.get('url', None)}\n\nLast price: {str(variables.get('last_price', None))}\nChange: {round(change, 2)}%""")
            msg['Subject'] = f"""💹 Price of {variables.get('prod_title', None)} went down!"""
        elif type is EmailTemplates.WATCH_STARTED:
            msg = MIMEText(
                f"""Watching offer {variables.get('url', None)} has started. You will be notified once the price has changed!\n\nInitial price: {variables.get('threshold_price', None)}""")
            msg['Subject'] = f"""ℹ️ Watching has started!"""
        elif type is EmailTemplates.WATCH_CANCELLED:
            msg = MIMEText(
                f"""
                    <html>
                    <head>
                        <style>
                            p {{
                                font-size: 16px;
                            }}
                        </style>
                    </head>
                        <body>
                            <p>
                                Watching offer {variables.get('url', None)} has been cancelled. 
                                Likely the offer has expired or been archived.
                            </p>
                            <br/>
                            <p>
                                Last found price: {variables.get('last_price', None)}
                            </p>
                            {'<br/>'.join(list(map(lambda src: f'<img src={src} width=500px/>', variables.get("images", []))))}
                        </body>
                    </html>
                """, 'html')
            msg['Subject'] = f"""🛑 Watching has been aborted!"""
        else:
            msg = MIMEText(
                """Unrecognized email template. Please notify development team""")

        return msg.as_string()

    @staticmethod
    def send_mail(
            variables={},
            to=[],
            type=''):
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
