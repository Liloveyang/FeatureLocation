#coding=utf-8
import sqlite3 as db
import numpy as np
import datetime
import io
from Method import  *
from Util import *

class Dataset:

    def __init__(self):

        self.sqlite_conn = db.connect("resource/ast.db", check_same_thread=False)
        self.cursor = self.sqlite_conn.cursor()
        self.initialDatabase()
        sql = "select name, className, content from methodinfo "
        self.methods = []
        self.methodNames = []
        for methodinfo in self.executequery(sql):
            self.methods.append( Method(methodinfo))
            self.methodNames.append(methodinfo[0])
        sql ='select callMethodName, calledMethodName from methodInvocationinfo'
        self.invocations = []
        for invocation in self.executequery(sql):
            self.invocations.append(MethodInovation(invocation) )

        sql = 'select ID,origiMethods, methods from goldSets '
        self.goldSet =[]
        for item in self.executequery(sql):
            self.goldSet.append(GoldSet(item))

    def initialDatabase(self):
        fo = open('resource/createTables.sql', 'r')
        fc = fo.readlines()
        fo.close()
        str = " ".join(fc)
        statements = str.split(';')
        for statement in statements:
            self.execute(statement)
        fo = open('resource/createIndexs.sql','r')
        fc = fo.readlines()
        fo.close()
        str = " ".join(fc).lower()
        statements = str.split(';')
        for statement in statements:
            begin = statement.find("[")
            end  = statement.find("]")
            name = statement[begin+1: end]
            sql = "SELECT name FROM sqlite_master WHERE type = 'index' and name = '%s'" % name
            result = self.executequery(sql)
            if len(result) == 0:
                self.execute(statement)
        self.commit()



    def __del__(self):
        self.cursor.close()
        self.sqlite_conn.close()

    #获取偏好集合
    def getLikingList(self):
        return {}

    #获取厌恶集合
    def getDisLikingList(self):
        return {}

    def getGoldSets(self):
        return self.goldSet

    def getEntrancePoint(self):
        sql = "select ID, methods from entrancePointInfo"
        entrancepoints = []
        for entrancepoint in self.executequery(sql):
            entrancepoints.append(EntrancePoint(entrancepoint))
        return entrancepoints

    #获取项目中所有的方法调用
    def getAllMethodInvocation(self):
        return self.invocations

    #获取项目中所有方法名称
    def getAllMethodName(self):
        return self.methodNames

    #获取项目中所有的方法
    def getAllMethod(self):
        return self.methods

    def getAllInvocateMethod(self):
        sql = "select name from methodinfo where name in (  select callmethodname from methodinvocationinfo  union select calledmethodname from methodinvocationinfo )"
        return self.executequery(sql)

    def getMethodIndex(self, methodName):
        return self.methodNames.index(methodName)

    def getCallBy(self, methodName):
        sql = "select calledMethodName where callMethodName = % " % methodName
        methods = []
        for name in self.executequery(sql):
            methods.appnd( name[0] )
        return methods



    def execute(self, query):
        return self.cursor.execute(query)

    def executemany(self, sql, content):
        return self.cursor.executemany(sql, content)

    def commit(self):
        self.sqlite_conn.commit()

    def executequery(self, query):
        result = self.cursor.execute(query)
        result = result.fetchall()
        return result

               #计算距离依赖相似度
    def simiDist(self, m1, m2):
        sql = 'select length from simDistance where callMethodName = "%s" and calledMethodName = "%s"'%(m1,m2)
        length = self.executequery(sql)
        if len(length)  == 0: return 0
        return np.power(0.7,length[0])


     #计算上下文依赖相似度
    def simiContext(self, m1, m2):
        begin = datetime.datetime.now()
        #被m1调用的方法 intersect 被m2调用的方法集合
        sql = 'select calledMethodname from methodinvocationinfo where callmethodName = "%s" ' % m1
        calledmethod_m1 = set(self.executequery(sql))
        sql = 'select calledMethodname from methodinvocationinfo where callmethodName = "%s" ' %  m2
        calledmethod_m2 = set(self.executequery(sql))
        calledintersect = calledmethod_m1.intersection(calledmethod_m2)
        calledunion = calledmethod_m1.union(calledmethod_m2)
        begin = showDuration(begin, "called")
        #调用m1的方法集合 intersect 调用m2的方法集合
        sql = 'select callMethodname from methodinvocationinfo where calledmethodName = "%s"' % m1
        callmethod_m1 = set(self.executequery(sql))
        sql ='select callMethodname from methodinvocationinfo where calledmethodName = "%s" ' %  m2
        callmethod_m2 = set(self.executequery(sql))
        callintersect = callmethod_m1.intersection(callmethod_m2)
        callunion = callmethod_m1.union(callmethod_m2)
        begin = showDuration(begin, "call")
        #被m1访问的成员变量 intersect 被m2 访问的成员变量集合
        sql = 'select name from variableinfo where  isField = 1 and belongedMethod = "%s"' % m1
        access_m1 = set(self.executequery(sql))
        sql = 'select name from variableinfo where  isField = 1 and belongedMethod = "%s"' %  m2
        access_m2 = set(self.executequery(sql))
        accessintersect = access_m1.intersection(access_m2)
        accessunion = access_m1.union(access_m2)
        begin = showDuration(begin, "access")
        if ( len(callunion) + len(calledunion) + len(accessunion)) == 0 : return 0
        return ( len(callintersect) + len(calledintersect) + len(accessintersect)) / ( len(callunion) + len(calledunion) + len(accessunion))

ds = Dataset()
ds.initialDatabase()



