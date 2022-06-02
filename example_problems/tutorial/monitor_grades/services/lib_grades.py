#!/usr/bin/env python3

from Token import Token
from FolderData import FolderData
from FileData import FileData

from os import listdir
import os
import re

ALLPROBLEM = "all_problems"
ALLSERVICE = "all_services"
ALLSTUDENT = "all_students"
OKCONSTANT = "OK"
NOCONSTANT = "NO"


class lib_grades(object):
    def __init__(self) -> None:
        self.problemlist = Token()

    def loadFile(
        self, problem: str, service: str, token: str, path: str, regex_filename: str
    ):
        for x in listdir(path):
            fullpath = os.path.join(path, x)
            if os.path.isdir(fullpath):
                folderdata = FolderData(x, fullpath)

                if Token.isSameToken(folderdata.token, token, ALLSTUDENT):
                    for y in listdir(fullpath):
                        fullfilename = os.path.join(fullpath, y)

                        if os.path.isfile(fullfilename) and re.match(regex_filename, y):
                            filedata = FileData(y, fullfilename, folderdata)

                            if (
                                filedata.folderdata.problem == problem
                                or problem == ALLPROBLEM
                            ):
                                if (
                                    filedata.folderdata.service == service
                                    or service == ALLSERVICE
                                ):
                                    self.problemlist.addToken(filedata)

        self.problemlist.listSort()

    def getProblemList(self):
        return self.problemlist
