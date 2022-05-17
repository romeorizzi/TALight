#!/usr/bin/env python3

from FileData import FileData
from Goal import Goal

class Service(object):
    def __init__(self,  service : str):
        self.goals = list()
        self.service = service

    def addGoal(self, filedata : FileData):
        for x in self.goals:
            if x.goal == filedata.goal:
                x.addContent(filedata)
                return

        g = Goal(filedata.goal)
        g.addContent(filedata)
        self.goals.append(g)
    
    def listSort(self):
        self.goals.sort(key=Service.sortFunction)
        
        for x in self.goals:
            x.listSort()

    def sortFunction(v : Goal):
        return v.goal
