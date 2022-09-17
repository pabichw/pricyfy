'''sender module'''
import smtplib


class Sender:
    '''Sender'''
    @staticmethod
    def compose_mail(prod_title, price, last_price, url):
        '''compose mail'''
        print('prodTitle', prod_title, 'price', price, 'url', url)
        return 'Subject: Price of' + str(prod_title.encode('utf-8')) + ' went down!\n\nPrice of ' + str(prod_title.encode('utf-8')) + ' has just went down to ' + str(
            price) + '! There is a direct link:' + str(url.encode('utf-8')) + '\nLast price: ' + str(last_price)

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
