from FolderData import FolderData

class FileData(object):  
    def __init__(self, filename : str, fullpath : str, folderdata : FolderData):
        self.fullpath = fullpath

        s = str(filename).split('_')
        goal = s[1].split('.')[0]

        self.result = s[0]
        self.goal = goal

        file_descriptor = open(self.fullpath)
        self.content = file_descriptor.read()

        self.folderdata = folderdata

    def isDone(self):
        return self.result == "OK"
