#!/usr/bin/env python3

from FileData import FileData
from Structure import Structure


class Token(object):
    @staticmethod
    def isTeacher(s: str) -> str:
        return s[0] == "_"

    @staticmethod
    def takeName(s: str) -> str:
        if "_" in s:
            if Token.isTeacher(s):
                return Token.takeUserName(s)
            else:
                return Token.takeNumberVR(s) + "_" + Token.takeGIAUsername(s)
        else:
            return s

    @staticmethod
    def takeUserName(s: str) -> str:
        if "_" in s:
            res = s.split("_")
            if len(res[len(res) - 2]) == 10:
                return res[len(res) - 1]
            else:
                return res[len(res) - 1 - 1] + "_" + res[len(res) - 1]
        else:
            return ""

    @staticmethod
    def isSameToken(tokenfolder: str, token: str, ALLSTUDENT) -> bool:
        if token == ALLSTUDENT:
            return True

        if (
            not Token.isTeacher(token) and not Token.isTeacher(tokenfolder)
        ) and not "_" in token:
            if Token.takeNumberVR(tokenfolder) == Token.takeNumberVR(token):
                return True

        return Token.takeName(tokenfolder) == Token.takeName(token)

    @staticmethod
    def takeNumberVR(token: str):
        if Token.isTeacher(token):
            return ""
        else:
            return token.split("_")[0]

    @staticmethod
    def takeGIAUsername(token: str):
        if Token.isTeacher(token):
            return ""
        else:
            return token.split("_")[1]

    def __init__(self):
        self.tokens = list()

    def addToken(self, filedata: FileData):
        for x in self.tokens:
            if x.token == filedata.folderdata.token:
                x.addFile(filedata)
                return

        s = Structure(filedata.folderdata.token)
        s.addFile(filedata)
        self.tokens.append(s)

    def printToConsole(self, printAll: bool = False):
        for e in self.tokens:
            struser = Token.takeName(e.token)

            print("Student: " + struser)
            print("========================")

            for x in e.problem:
                for y in x.services:
                    print(x.problem, y.service, sep=": ")

                    for z in y.goals:
                        print(z.goal, sep=": ", end="")

                        if printAll:
                            print("->")
                            for o in z.content:
                                print("\t", o.toString(), sep="")
                        else:
                            print("->", z.getLastContent().toString())

            print()

    def listSort(self):
        self.tokens.sort(key=Token.sortFunction)

        for x in self.tokens:
            x.listSort()

    def sortFunction(v: Structure):
        return v.token

    def instanceToString(self, printAll: bool = False):
        lines = list()

        for e in self.tokens:
            for x in e.problem:
                for y in x.services:
                    for z in y.goals:
                        if printAll:
                            for o in z.content:
                                line = (
                                    e.token
                                    + ","
                                    + x.problem
                                    + ","
                                    + y.service
                                    + ","
                                    + z.goal
                                    + ","
                                    + o.toString(",")
                                    + "\n"
                                )
                                lines.append(line)
                        else:
                            if z.getStatusContent():
                                value = "OK"
                            else:
                                value = "NO"

                            line = (
                                Token.takeName(e.token)
                                + ","
                                + x.problem
                                + ","
                                + y.service
                                + ","
                                + z.goal
                                + ","
                                + value
                                + ","
                                + z.getLastContent().toStringDate()
                                + "\n"
                            )
                            lines.append(line)

        return "".join(str(i) for i in lines)

    def tupleToTable(header, t, m=-1):
        if type(t) == tuple:
            l = list()
            l.append(t)
            return Token.tupleToTable(header, l, m)
        elif type(t) == int:
            l = list()
            l.append(t)
            return Token.tupleToTable(header, l, m)
        else:
            if m == -1:
                if len(t) != 0 and type(t[0]) != int:
                    n = len(t[0])
                else:
                    n = 1
            else:
                n = m

        t.insert(0, header)

        max = 0
        if n > 1:
            for x in t:
                for j in x:
                    if len(str(j)) > max:
                        max = len(j) + 1
        else:
            max = 20

        max = str(max)
        if n == 1:
            for x in t:
                print(x)
        elif n == 2:
            for x in t:
                print(("{:<" + max + "}{}").format(x[0], x[1]))
        elif n == 3:
            for x in t:
                print(("{:<" + max + "}{:<" + max + "}{}").format(x[0], x[1], x[2]))
        elif n == 4:
            for x in t:
                print(
                    ("{:<" + max + "}{:<" + max + "}{:<" + max + "}{}").format(
                        x[0], x[1], x[2], x[3]
                    )
                )
        elif n == 5:
            for x in t:
                print(
                    (
                        "{:<" + max + "}{:<" + max + "}{:<" + max + "}{:<" + max + "}{}"
                    ).format(x[0], x[1], x[2], x[3], x[4])
                )
        else:
            raise

    @staticmethod
    def tupleToFile(t):
        lines = list()

        for i in t:
            s = ";".join(str(el) for el in i)
            lines.append(s)

        return "\n".join(str(i) for i in lines)

    def countTokenTries(self, mode: str):
        l = list()

        for for_token in self.tokens:
            total_tries = 0

            if mode == "num_total_gross_number":
                for for_problem in for_token.problem:
                    for for_service in for_problem.services:
                        for for_goal in for_service.goals:
                            for for_content in for_goal.content:
                                total_tries += 1
            elif mode == "num_total_different_submissions":
                for for_problem in for_token.problem:
                    for for_service in for_problem.services:
                        total_tries += 1
            else:
                raise

            l.append((Token.takeName(for_token.token), total_tries))

        return l

    def countTokenOkAndNoGoals(self):
        l = list()

        for for_token in self.tokens:
            ok_goals = 0
            no_goals = 0

            for for_problem in for_token.problem:
                for for_service in for_problem.services:
                    for for_goal in for_service.goals:
                        if for_goal.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

            l.append((Token.takeName(for_token.token), ok_goals, no_goals))

        return l

    def countProblemOkAndNoGoals(self, requirement: str):
        l = list()

        for for_token in self.tokens:
            resolvedproblem = 0

            for for_problem in for_token.problem:
                ok_goals = 0
                no_goals = 0

                for for_service in for_problem.services:
                    for for_goal in for_service.goals:
                        if for_goal.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

                if requirement == "num_problems_touched":
                    if ok_goals > 0 or no_goals > 0:
                        resolvedproblem += 1
                elif requirement == "num_problems_partial":
                    if ok_goals > 0:
                        resolvedproblem += 1
                elif requirement == "num_problems_full":
                    if no_goals == 0:
                        resolvedproblem += 1
                else:
                    if no_goals == 0:
                        resolvedproblem += 1

            l.append((Token.takeName(for_token.token), resolvedproblem))

        return l

    def countServiceOkAndNoGoals(self, requirement: str):
        l = list()

        for for_token in self.tokens:
            for for_problem in for_token.problem:
                resolvedservice = 0

                for for_service in for_problem.services:
                    ok_goals = 0
                    no_goals = 0

                    for for_goal in for_service.goals:
                        if for_goal.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

                    if requirement == "num_services_touched":
                        if ok_goals > 0 or no_goals > 0:
                            resolvedservice += 1
                    elif requirement == "num_services_partial":
                        if ok_goals > 0:
                            resolvedservice += 1
                    elif requirement == "num_services_full":
                        if no_goals == 0:
                            resolvedservice += 1
                    else:
                        if no_goals == 0:
                            resolvedservice += 1

                l.append(
                    (
                        Token.takeName(for_token.token),
                        for_problem.problem,
                        resolvedservice,
                    )
                )

        return l

    def countGoalsOkAndNoGoals(self):
        l = list()

        for for_token in self.tokens:
            for for_problem in for_token.problem:
                for for_service in for_problem.services:
                    resolvedgoal = 0

                    ok_goals = 0
                    no_goals = 0

                    for for_goal in for_service.goals:
                        if for_goal.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

                    if no_goals == 0:
                        resolvedgoal += 1

                    l.append(
                        (
                            Token.takeName(for_token.token),
                            for_problem.problem,
                            for_service.service,
                            resolvedgoal,
                        )
                    )

        return l

    def countTokenTriesWithoutStudent(self, mode: str):
        l = list()

        total_tries = 0

        for for_token in self.tokens:
            if mode == "num_total_gross_number":
                for for_problem in for_token.problem:
                    for for_service in for_problem.services:
                        for for_goal in for_service.goals:
                            for for_content in for_goal.content:
                                total_tries += 1
            elif mode == "num_total_different_submissions":
                for for_problem in for_token.problem:
                    for for_service in for_problem.services:
                        total_tries += 1
            else:
                raise

        l.append((total_tries))

        return l

    def countTokenOkAndNoGoalsWithoutStudent(self):
        l = list()

        ok_goals = 0
        no_goals = 0

        for for_token in self.tokens:
            for for_problem in for_token.problem:
                for for_service in for_problem.services:
                    for for_goal in for_service.goals:
                        if for_goal.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

        l.append((ok_goals, no_goals))

        return l

    def countProblemOkAndNoGoalsWithoutStudent(self, requirement: str):
        l = list()

        resolvedproblem = 0

        for for_token in self.tokens:
            for for_problem in for_token.problem:
                ok_goals = 0
                no_goals = 0

                for for_service in for_problem.services:
                    for for_goal in for_service.goals:
                        if for_goal.getStatusContent():
                            ok_goals += 1
                        else:
                            no_goals += 1

                if requirement == "num_problems_touched":
                    if ok_goals > 0 or no_goals > 0:
                        resolvedproblem += 1
                elif requirement == "num_problems_partial":
                    if ok_goals > 0:
                        resolvedproblem += 1
                elif requirement == "num_problems_full":
                    if no_goals == 0:
                        resolvedproblem += 1
                else:
                    if no_goals == 0:
                        resolvedproblem += 1

        l.append((resolvedproblem))

        return l

    def countServiceOkAndNoGoalsWithoutStudent(self, requirement: str):
        l = list()

        for out_for_token in self.tokens:
            for out_for_problem in out_for_token.problem:
                resolvedservice = 0

                for for_token in self.tokens:
                    for for_problem in for_token.problem:
                        if for_problem.problem == out_for_problem.problem:
                            for for_service in for_problem.services:
                                ok_goals = 0
                                no_goals = 0

                                for for_goal in for_service.goals:
                                    if for_goal.getStatusContent():
                                        ok_goals += 1
                                    else:
                                        no_goals += 1

                                if requirement == "num_services_touched":
                                    if ok_goals > 0 or no_goals > 0:
                                        resolvedservice += 1
                                elif requirement == "num_services_partial":
                                    if ok_goals > 0:
                                        resolvedservice += 1
                                elif requirement == "num_services_full":
                                    if no_goals == 0:
                                        resolvedservice += 1
                                else:
                                    if no_goals == 0:
                                        resolvedservice += 1

                l.append((out_for_problem.problem, resolvedservice))

            return l

    def countGoalsOkAndNoGoalsWithoutStudent(self):
        l = list()

        for out_for_token in self.tokens:
            for out_for_problem in out_for_token.problem:
                for out_for_service in out_for_problem.services:
                    resolvedgoal = 0

                    for for_token in self.tokens:
                        for for_problem in for_token.problem:
                            if for_problem.problem == out_for_problem.problem:
                                for for_service in for_problem.services:
                                    if for_service.service == out_for_service.service:
                                        ok_goals = 0
                                        no_goals = 0

                                        for for_goal in for_service.goals:
                                            if for_goal.getStatusContent():
                                                ok_goals += 1
                                            else:
                                                no_goals += 1

                                        if no_goals == 0:
                                            resolvedgoal += 1

                    l.append(
                        (out_for_problem.problem, out_for_service.service, resolvedgoal)
                    )

            return l
