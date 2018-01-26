class Method:
    def __init__(self, methodinfo):
        self.name,  self.className, self.content = methodinfo

class MethodInovation:
    def __init__(self, methodinvocationInfo):
        self.callMethod, self.calledMethod = methodinvocationInfo

class GoldSet:
    def __init__(self, goldset):
        self.ID, self.origiMethods , self.methods = goldset
class EntrancePoint:
    def __init__(self, entrancepoint):
        self.ID, self.methods = entrancepoint

class MethodList:
    def __init__(self, methods):
        self.methods = methods

    def index(self, methodname):
        for method in self.methods:
            if method.name == methodname:
                return self.methods.index(method)
        return -1
