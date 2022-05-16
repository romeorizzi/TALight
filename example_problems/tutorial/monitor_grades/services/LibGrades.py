#!/usr/bin/env python3

from Token import Token
from FolderData import FolderData
from FileData import FileData

from os import listdir
import os

ALLPROBLEM = "all_problems"
ALLSERVICE = "all_services"
OKCONSTANT = "OK"

class LibGrades(object):
    def __init__(self) -> None:
        self.problemlist = Token()

    def loadFile(self, problem : str, service : str, token : str, path : str):
        for x in listdir(path):
            fullpath = os.path.join(path, x)
            if (os.path.isdir(fullpath)):
                folderdata = FolderData(x, fullpath)

                # TODO Fix this
                if (folderdata.token == token or token == "all"):
                    for y in listdir(fullpath):
                        filedata = FileData(y, os.path.join(fullpath, y), folderdata)
                        
                        if (filedata.folderdata.problem == problem or problem == ALLPROBLEM):
                            if (filedata.folderdata.service == service or service == ALLSERVICE):
                                self.problemlist.addToken(filedata)

    def getProblemList(self):
        return self.problemlist