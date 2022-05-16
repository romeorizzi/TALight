#!/usr/bin/env python3

import time

class Content(object):
    def __init__(self,  data : str, content : str, result : bool):
        self.data = data
        self.content = content
        self.result = result
        
    def toString(self, sep=''):
        resultstr = "OK"
        if (self.result):
            resultstr = "OK"
        else:
            resultstr = "NO"
        return resultstr + " (" + self.toStringDate() + ")"

    def toStringDate(self):
        return time.strftime('%Y-%m-%d %H-%M-%S', self.data)
