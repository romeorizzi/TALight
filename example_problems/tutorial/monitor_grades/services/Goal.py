#!/usr/bin/env python3

from FileData import FileData
from Content import Content


class Goal(object):
    def __init__(self, goal: str):
        self.content = list()
        self.goal = goal

    def addContent(self, filedata: FileData):
        c = Content(filedata.folderdata.date, filedata.content, filedata.isDone())
        self.content.append(c)

    def getStatusContent(self):
        for x in self.content:
            if x.result:
                return True

        return False

    def getLastContent(self):
        for x in self.content:
            if x.result:
                return x

        if len(self.content) > 0:
            return self.content[0]
        else:
            return None

    def listSort(self):
        self.content.sort(key=Goal.sortFunction)

    def sortFunction(v: Content):
        return v.data
