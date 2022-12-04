'''logger module'''


class Logger:
    '''Logger module'''
    @staticmethod
    def log(id, content):
        '''log'''

        try:
            with open(f'logs/{id}.txt', "a+") as myfile:
                myfile.write(f'{content}\n')
                myfile.close()

        except e:
            print('e', e)
