#!/usr/bin/env python3

from FileData import FileData
from Structure import Structure

class Token(object):
    def __init__(self):
        self.tokens = list()

    def addToken(self, filedata : FileData):
        for x in self.tokens:
            if x.token == filedata.folderdata.token:
                x.addFile(filedata)
                return

        s = Structure(filedata.folderdata.token)
        s.addFile(filedata)
        self.tokens.append(s)
        
    def printToConsole(self, printAll : bool = False):
        for e in self.tokens:
            print("Student: " + e.token)
            print("========================")

            for x in e.problem:
                for y in x.services:
                    print(x.problem, y.service, sep=': ')

                    for z in y.goals:
                        print(z.goal, sep=': ', end = '')

                        if printAll:
                            for o in z.content:
                                print('->', o.toString())
                        else:
                            value = ""
                            if z.getStatusContent():
                                value = "OK"
                            else:
                                value = "NO"

                            print('->', value)

            print()

    def instanceToString(self, printAll : bool = False):
        lines = list()

        for e in self.tokens:
            for x in e.problem:
                for y in x.services:
                    for z in y.goals:
                        if printAll:                       
                            for o in z.content: 
                                line = e.token + "," + x.problem + "," + y.service + "," + z.goal + "," + o.toString(',') + '\n'
                                lines.append(line)
                        else:
                            value = ""
                            if z.getStatusContent():
                                value = "OK"
                            else:
                                value = "NO"

                            line = e.token + "," + x.problem + "," + y.service + "," + z.goal + "," + value + "\n"

        return ''.join(str(i) for i in lines)

    def countTokenTries(self):
        l = list()

        for e in self.tokens:
            total_tries = 0

            for x in e.problem:
                for y in x.services:
                    for z in y.goals:
                        total_tries += 1

            l.append((e.token, total_tries))

        return l

    def countTokenOkAndNoGoals(self):
        l = list()

        for e in self.token:
            ok_goals = 0
            no_goals = 0

            for x in e.problem:
                for y in x.services:
                    for z in y.goals:
                        if z.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

                l.append((e.token, ok_goals, no_goals))

        return l

    def countProblemOkAndNoGoals(self):
        l = list()

        for e in self.token:
            for x in e.problem:
                ok_goals = 0
                no_goals = 0

                for y in x.services:
                    for z in y.goals:
                        if z.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

                l.append((e.token, x.problem, ok_goals, no_goals))

        return l

    def countServiceOkAndNoGoals(self):
        l = list()

        for e in self.token:
            for x in e.problem:
                for y in x.services:
                    ok_goals = 0
                    no_goals = 0

                    for z in y.goals:
                        if z.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

                    l.append((e.token, x.problem, e.service, ok_goals, no_goals))

        return l
