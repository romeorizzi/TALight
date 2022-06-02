#!/usr/bin/env python3

from FileData import FileData
from Service import Service


class Problem(object):
    def __init__(self, problem: str):
        self.services = list()
        self.problem = problem

    def addService(self, filedata: FileData):
        for x in self.services:
            if x.service == filedata.folderdata.service:
                x.addGoal(filedata)
                return

        t = Service(filedata.folderdata.service)
        t.addGoal(filedata)
        self.services.append(t)

    def listSort(self):
        self.services.sort(key=Problem.sortFunction)

        for x in self.services:
            x.listSort()

    def sortFunction(s: Service):
        return s.service
