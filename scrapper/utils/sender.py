'''sender module'''
import smtplib
import os
from email.mime.text import MIMEText


class Sender:
    '''Sender'''
    @staticmethod
    def compose_mail(prod_title, price, last_price, url, to):
        '''compose mail'''
        msg = MIMEText(f"""Price of {prod_title} has just went down to 
                          {str(price)}\n\nThere is a direct link: {url}\n\nLast price: {str(last_price)}""")
        msg['Subject'] = f"""Subject: 💹 Price of {prod_title}  went down!"""
        msg['From'] = os.environ.get("SMTP_FROM")
        # msg['To'] = ", ".join(to)
        return msg.as_string()

    @ staticmethod
    def send_mail(
            prod_title,
            price,
            last_price,
            url,
            to=[]):
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
                prod_title,
                price,
                last_price,
                url,
                to))
        server.quit()
