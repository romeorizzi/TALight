#!/usr/bin/env python3

from FileData import FileData
from Problem import Problem


class Structure(object):
    def __init__(self, token: str):
        self.problem = list()
        self.token = token

    def addFile(self, filedata: FileData):
        for x in self.problem:
            if x.problem == filedata.folderdata.problem:
                x.addService(filedata)
                return

        p = Problem(filedata.folderdata.problem)
        p.addService(filedata)
        self.problem.append(p)

    def listSort(self):
        self.problem.sort(key=Structure.sortFunction)

        for x in self.problem:
            x.listSort()

    def sortFunction(v: Problem):
        return v.problem
