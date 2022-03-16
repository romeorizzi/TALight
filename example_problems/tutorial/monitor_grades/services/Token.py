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
        
    def printToConsole(self):
        for e in self.tokens:
            print("Student: " + e.token)
            print("========================")

            for x in e.problem:
                print(x.problem)

                for y in x.services:
                    print('\t' + y.service)

                    for z in y.goals:
                        print('\t' + '\t' + z.goal)

                        for o in z.content:
                            print('\t' + '\t' + '\t' + ' -> ' + o.toString())

                        print('\n')

    def instanceToFile(self):
        lines = list()

        for e in self.tokens:
            for x in e.problem:
                for y in x.services:
                    for z in y.goals:
                        for o in z.content: 
                            line = e.token + "," + x.problem + "," + y.service + "," + z.goal + "," + o.data + "," + o.content
                            lines.append(line)

        return ''.join(str(i) for i in lines)
