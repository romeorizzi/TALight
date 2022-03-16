import time

class FolderData(object):
    def __init__(self, datafile : str, fullpath : str):       
        self.fullpath = fullpath
        
        s = str(datafile).split('+')

        self.token = s[0]
        self.date = time.strptime(s[1], '%Y-%m-%d_%H-%M-%S_%f')
