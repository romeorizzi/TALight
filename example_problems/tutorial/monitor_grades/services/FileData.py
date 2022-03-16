from FolderData import FolderData

class FileData(object):  
    def __init__(self, filename : str, fullpath : str, folderdata : FolderData):
        self.fullpath = fullpath

        s = str(filename).split('_')
        goal = s[3].split('.')[0]

        self.result = s[0]
        self.problem = s[1]
        self.service = s[2]
        self.goal = goal

        file_descriptor = open(self.fullpath)
        self.content = file_descriptor.read()

        self.folderdata = folderdata
