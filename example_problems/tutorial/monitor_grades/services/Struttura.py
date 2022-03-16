from FileData import FileData
from Problem import Problem

class Struttura(object):
    def __init__(self):
        self.problem = list()

    def addFile(self, filedata : FileData):
        for x in self.problem:
            if x.problem == filedata.problem:
                x.addService(filedata)
                return

        p = Problem(filedata.problem)
        p.addService(filedata)
        self.problem.append(p)

    def printToConsole(self):
        for x in self.problem:
            print(x.problem)

            for y in x.services:
                print('\t', y.service, sep='')

                for z in y.goals:
                    print('\t', '\t', z.goal, sep='')

                    for o in z.content:
                        print('\t', '\t', '\t', ' -> ', o.toString(), sep='')

                    print('\n')
                    