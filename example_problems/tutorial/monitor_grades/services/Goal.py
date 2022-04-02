from FileData import FileData
from Content import Content

class Goal(object):
    def __init__(self, goal : str):
        self.content = list()
        self.goal = goal

    def addContent(self, filedata : FileData):
        c = Content(filedata.folderdata.date, filedata.content, filedata.isDone())
        self.content.append(c)
        
    def getStatusContent(self):
        done = False
        for x in self.content:
            if x.result:
                done = True

        return done
        