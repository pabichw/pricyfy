'''logger module'''


class Logger:
    '''Logger module'''
    @staticmethod
    def log(id, content, format = 'txt'):
        '''log'''

        try:
            with open(f'logs/{id}.{format}', "a+") as myfile:
                myfile.write(f'{content}\n')
                myfile.close()

        except e:
            print('e', e)
