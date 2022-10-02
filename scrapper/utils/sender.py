'''sender module'''
import smtplib


class Sender:
    '''Sender'''
    @staticmethod
    def compose_mail(prod_title, price, last_price, url):
        '''compose mail'''
        return ('Subject: 💹 Price of ' + prod_title + ' went down!\n\nPrice of ' + prod_title + ' has just went down to '
                + str(price) + '!\n\nThere is a direct link:' +
                url + '\n\nLast price: ' +
                str(last_price)).encode('utf-8').strip()

    @staticmethod
    def send_mail(
            prod_title,
            price,
            last_price,
            url,
            to='pabichwiktor@gmail.com'):
        '''send mail'''
        server = smtplib.SMTP('mail28.mydevil.net', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('bot@pabich.cc', 'Prometeusz213')  # TODO: Hash it
        server.sendmail(
            'bot@pabich.cc',
            to,
            Sender.compose_mail(
                prod_title,
                price,
                last_price,
                url))
        server.quit()
