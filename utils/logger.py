import smtplib

class Logger:

    @staticmethod
    def log(id, content):
        print('Logging for ', id, 'content', content)

        try:
            with open(f'logs/{id}.txt', "a+") as myfile:
                myfile.write(f'{content}\n')
                myfile.close()

        except e:
            print('e', e)
