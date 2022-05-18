#!/usr/bin/env python3

from Token import Token
from FolderData import FolderData
from FileData import FileData

from os import listdir
import os

ALLPROBLEM = "all_problems"
ALLSERVICE = "all_services"
ALLSTUDENT = "all_students"
OKCONSTANT = "OK"
NOCONSTANT = "NO"

class lib_grades(object):
    def __init__(self) -> None:
        self.problemlist = Token()

    def loadFile(self, problem : str, service : str, token : str, path : str):
        token = lib_grades.getTokenUser(token)

        for x in listdir(path):
            fullpath = os.path.join(path, x)
            if (os.path.isdir(fullpath)):
                folderdata = FolderData(x, fullpath)

                nametoken = lib_grades.getTokenUser(folderdata.token)

                if (nametoken == token or token == ALLSTUDENT):
                    for y in listdir(fullpath):
                        filedata = FileData(y, os.path.join(fullpath, y), folderdata)
                        
                        if (filedata.folderdata.problem == problem or problem == ALLPROBLEM):
                            if (filedata.folderdata.service == service or service == ALLSERVICE):
                                self.problemlist.addToken(filedata)

        self.problemlist.listSort()        

    def getProblemList(self):
        return self.problemlist

    @staticmethod
    def hideToken(s : str) -> str:
        if "__" in s:
            return s.split('__')[1]
        else:
            return s.split('_')[1]

    @staticmethod
    def isTeacher(s : str) -> str:
        return "__" in s

    @staticmethod
    def getTokenUser(token) -> str:
        if (token == ALLSTUDENT):
            return token

        if ("__" in token):
            return token.split('__')[1]
        elif ("_" in token):
            return token.split('_')[1]
        else:
            return token