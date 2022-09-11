import smtplib


class Sender:
    @staticmethod
    def composeMail(prodTitle, price, url):
        print('prodTitle', prodTitle, 'price', price, 'url', url)
        return 'Subject: Price of' + str(prodTitle.encode('utf-8')) + ' went down!\n\nPrice of' + str(prodTitle.encode('utf-8')) + 'has just went down to ' + str(price) + '! There is a direct link:' + str(url.encode('utf-8'))

    @staticmethod
    def send_mail(prodTitle, price, url, to='pabichwiktor@gmail.com'):
        server = smtplib.SMTP('mail28.mydevil.net', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('bot@pabich.cc', 'Prometeusz213')  # TODO: Hash it
        server.sendmail('bot@pabich.cc', to, Sender.composeMail(prodTitle, price, url))
        server.quit()
