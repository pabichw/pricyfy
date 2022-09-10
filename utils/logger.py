import smtplib

class Logger:

    @staticmethod
    def log(id, content):
        print('Logging for ', id)

        with open(f'logs/{id}.txt', "a+") as myfile:
            myfile.write(content)
