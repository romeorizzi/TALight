from FileData import FileData
from Problem import Problem

class Structure(object):
    def __init__(self, token : str):
        self.problem = list()
        self.token = token

    def addFile(self, filedata : FileData):
        for x in self.problem:
            if x.problem == filedata.problem:
                x.addService(filedata)
                return

        p = Problem(filedata.problem)
        p.addService(filedata)
        self.problem.append(p)
