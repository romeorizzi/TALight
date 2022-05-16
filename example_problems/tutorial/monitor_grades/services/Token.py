#!/usr/bin/env python3

import re
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
            struser = Token.hideToken(e.token)

            print("Student: " + struser)
            print("========================")

            for x in e.problem:
                for y in x.services:
                    print(x.problem, y.service, sep=': ')

                    for z in y.goals:
                        print(z.goal, sep=': ', end = '')

                        if printAll:
                            print('->')
                            for o in z.content:
                                print('\t', o.toString(), sep='')
                        else:
                            print('->', z.getLastContent().toString())

            print()

    def hideToken(s : str) -> str:
        if "__" in s:
            return s.split('__')[1]
        else:
            return s.split('_')[1]

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
                            if z.getStatusContent():
                                value = "OK"
                            else:
                                value = "NO"

                            line = Token.hideToken(e.token) + "," + x.problem + "," + y.service + "," + z.goal + "," + value + "," + z.toStringDate() + "\n"
                            lines.append(line)

        return ''.join(str(i) for i in lines)

    def tupleToTable(t, m = -1):
        if type(t) == tuple:
            l = list()
            l.append(t)
            return Token.tupleToTable(l, m)
        else:
            if m == -1:
                n = len(t[0])
            else:
                n = m

        if n == 2:
            for x in t:
                print("{:<14}{}".format(x[0], x[1]))
        elif n == 3:
            for x in t:
                print("{:<14}{:<14}{}".format(x[0], x[1], x[2]))
        elif n == 4:
            for x in t:
                print("{:<14}{:<14}{:<14}{}".format(x[0], x[1], x[2], x[3]))
        elif n == 5:
            for x in t:
                print("{:<14}{:<14}{:<14}{:<14}{}".format(x[0], x[1], x[2], x[3], x[4]))
        else:
            raise

    def tupleToFile(t):
        lines = list()

        for i in t:
            s = ";".join(str(el) for el in i)
            lines.append(s)

        return '\n'.join(str(i) for i in lines)

    def countTokenTries(self, mode : str):
        l = list()

        for e in self.tokens:
            total_tries = 0

            if (mode == "total_gross_number"):
                for x in e.problem:
                    for y in x.services:
                        for z in y.goals:
                            for c in z.content:
                                total_tries += 1
            elif (mode == "number_different_submissions"):
                for x in e.problem:
                    for y in x.services:
                        total_tries += 1
            else:
                raise

            l.append((Token.hideToken(e.token), total_tries))

        return l

    def countTokenOkAndNoGoals(self):
        l = list()

        for e in self.tokens:
            ok_goals = 0
            no_goals = 0

            for x in e.problem:
                for y in x.services:
                    for z in y.goals:
                        if z.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

            l.append((Token.hideToken(e.token), ok_goals, no_goals))

        return l

    def countProblemOkAndNoGoals(self, requirement : str):
        l = list()

        for e in self.tokens:
            resolvedproblem = 0

            for x in e.problem:
                ok_goals = 0
                no_goals = 0

                for y in x.services:
                    for z in y.goals:
                        if z.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

                if (requirement == "at_least_one_submission"):
                    if (ok_goals > 0 or no_goals > 0):
                        resolvedproblem += 1
                elif (requirement == "at_least_one_goal_achieved"):
                    if (ok_goals > 0):
                        resolvedproblem += 1
                elif (requirement == "at_least_one_service_fullfilled"):                    
                    if (no_goals == 0):
                        resolvedproblem += 1
                else:
                    raise

            l.append((Token.hideToken(e.token), resolvedproblem))

        return l

    def countServiceOkAndNoGoals(self):
        l = list()

        for e in self.tokens:
            for x in e.problem:
                resolvedservice = 0

                for y in x.services:
                    ok_goals = 0
                    no_goals = 0
                
                    for z in y.goals:
                        if z.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

                    if no_goals == 0:
                        resolvedservice += 1
                
                l.append((Token.hideToken(e.token), x.problem, resolvedservice))

        return l

    def countGoalsOkAndNoGoals(self):
        l = list()

        for e in self.tokens:
            for x in e.problem:
                for y in x.services:                
                    resolvedgoal = 0

                    ok_goals = 0
                    no_goals = 0
                
                    for z in y.goals:
                        if z.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

                    if no_goals == 0:
                        resolvedgoal += 1
                
                    l.append((Token.hideToken(e.token), x.problem, y.service, resolvedgoal))

        return l