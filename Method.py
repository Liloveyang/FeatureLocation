#用于对从数据库读出的数据进行简单的包装
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

class RecommendResult:
    def __init__(self, recommendresult):
        self.ID,self.methodName, self.islike, self.rounds, self.precision, self.recall,  self.fmeasure = recommendresult

    def __init__(self, ID, rounds ):
        self.ID = ID
        self.rounds = rounds

class MethodList:
    def __init__(self, methods):
        self.methods = methods


    def index(self, methodname):
        for method in self.methods:
            if method.name == methodname:
                return self.methods.index(method)
        return -1
