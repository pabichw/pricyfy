import smtplib


class Sender:
    @staticmethod
    def composeMail(prodTitle, price, url):
        return f'Subject: Price of {prodTitle} went down!\n\nPrice of {prodTitle} has just went down to {price}! There is a direct link: {url}'.encode(
            'utf-8')

    @staticmethod
    def send_mail(prodTitle, price, url):
        server = smtplib.SMTP('mail28.mydevil.net', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('bot@pabich.cc', 'Prometeusz213')  # TODO: Hash it
        server.sendmail('bot@pabich.cc', 'pabichwiktor@gmail.com', Sender.composeMail(prodTitle, price, url))
        server.quit()
