#coding=utf-8
import sqlite3 as db
import numpy as np
import datetime
from Method import  *
from Util import *

class Dataset:

    def __init__(self):
        self.sqlite_conn = db.connect("resource/ast.db")
        self.cursor = self.sqlite_conn.cursor()
        self.cursor.execute("select name, className, content from methodinfo")
        self.methods = []
        for methodinfo in self.cursor.fetchall():
            self.methods.append( Method(methodinfo) )

        self.cursor.execute('select callMethodName, calledMethodName from methodInvocationinfo')
        self.invocations = []
        for invocation in self.cursor.fetchall():
            self.invocations.append(MethodInovation(invocation) )

        self.cursor.execute('select ID,origiMethods, methods from goldSets ')
        self.goldSet =[]
        for item in self.cursor.fetchall():
            self.goldSet.append(GoldSet(item))


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
        self.cursor.execute("select ID, methods from entrancePointInfo")
        entrancepoints = []
        for entrancepoint in self.cursor.fetchall():
            entrancepoints.append(EntrancePoint(entrancepoint))
        return entrancepoints

    #获取项目中所有的方法调用
    def getAllMethodInvocation(self):
        return self.invocations


    #获取项目中所有的方法
    def getAllMethod(self):
        return self.methods

    def getAllInvocateMethod(self):
        self.cursor.execute("select name from methodinfo where name in (  select callmethodname from methodinvocationinfo  union select calledmethodname from methodinvocationinfo )")
        return self.cursor.fetchall()

    def getDemo(self):
        documents =[]
        documents.append("China supports DPRK, ROK in fostering trust, building consensus through dialogue")
        documents.append("Media reported that the DPRK and ROK Wednesday agreed to let their athletes march together under the unified flag of the Korean Peninsula at the opening ceremony of the Pyeongchang Winter Olympics next month.")
        documents.append("The agreement was reached at vice ministerial-level talks between the two countries, which were held Wednesday at Peace House, a building on the South Korean side of Panmunjom which straddles the heavily guarded border.")
        documents.append("Meanwhile, ROK Foreign Minister Kang Kyung-wha said the ROK will push forward dialogue for the peaceful resolution of the nuclear issue on the Korean Peninsula.")
        return documents


    def getMethodIndex(self, methodName):
        for i in range(0, len(self.methods)):
            if self.methods[i].name == methodName:
                return i


    def getCallBy(self, methodName):
        self.cursor.execute("select calledMethodName where callMethodName = % " % methodName)
        methods = []
        for name in self.cursor.fetchall():
            methods.appnd( name[0] )
        return methods



    def execute(self, query):
        return self.cursor.execute(query)

    def executemany(self, sql, content):
        return self.cursor.executemany(sql, content)

    def commit(self):
        self.sqlite_conn.commit()

               #计算距离依赖相似度
    def simiDist(self, m1, m2):
        sql = 'select length from simDistance where callMethodName = "%s" and calledMethodName = "%s"'%(m1,m2)
        sqlresult = self.execute(sql)
        length = sqlresult.fetchone()
        if length == None: return 0
        return np.power(0.7,length)


     #计算上下文依赖相似度
    def simiContext(self, m1, m2):
        #被m1调用的方法 intersect 被m2调用的方法集合
        sql = 'select calledMethodname from methodinvocationinfo where callmethodName = "%s" ' % m1
        self.execute(sql)
        calledmethod_m1 = set(self.cursor.fetchall())
        sql = 'select calledMethodname from methodinvocationinfo where callmethodName = "%s" ' %  m2
        self.execute(sql)
        calledmethod_m2 = set(self.cursor.fetchall())
        calledintersect = calledmethod_m1.intersection(calledmethod_m2)
        calledunion = calledmethod_m1.union(calledmethod_m2)
        #调用m1的方法集合 intersect 调用m2的方法集合
        sql = 'select callMethodname from methodinvocationinfo where calledmethodName = "%s"' % m1
        self.execute(sql)
        callmethod_m1 = set(self.cursor.fetchall())
        sql ='select callMethodname from methodinvocationinfo where calledmethodName = "%s" ' %  m2
        self.execute(sql)
        callmethod_m2 = set(self.cursor.fetchall())
        callintersect = callmethod_m1.intersection(callmethod_m2)
        callunion = callmethod_m1.union(callmethod_m2)

        #被m1访问的成员变量 intersect 被m2 访问的成员变量集合
        sql = 'select name from variableinfo where  isField = 1 and belongedMethod = "%s"' % m1
        self.execute(sql)
        access_m1 = set(self.cursor.fetchall())
        sql = 'select name from variableinfo where  isField = 1 and belongedMethod = "%s"' %  m2
        self.execute(sql)
        access_m2 = set(self.cursor.fetchall())
        accessintersect = access_m1.intersection(access_m2)
        accessunion = access_m1.union(access_m2)
        return ( len(callintersect) + len(calledintersect) + len(accessintersect)) / ( len(callunion) + len(calledunion) + len(accessunion))




'''
  #计算上下文依赖相似度
    def simiContext(self, m1, m2):
        #调用m1的方法集合 intersect 调用m2的方法集合
        sql = 'select callMethodname from methodinvocationinfo where calledmethodName = "%s" intersect select callMethodname from methodinvocationinfo where calledmethodName = "%s" ' % (m1, m2)
        self.execute(sql)
        callintersect = self.cursor.fetchall()
        #被m1调用的方法 intersect 被m2调用的方法集合
        sql = 'select calledMethodname from methodinvocationinfo where callmethodName = "%s" intersect select calledMethodname from methodinvocationinfo where callmethodName = "%s" ' % (m1, m2)
        self.execute(sql)
        calledintersect = self.cursor.fetchall()
        #被m1访问的成员变量 intersect 被m2 访问的成员变量集合
        sql = 'select name from variableinfo where  isField = 1 and belongedMethod = "%s" intersect select name from variableinfo where  isField = 1 and belongedMethod = "%s"' % (m1, m2)
        self.execute(sql)
        accessintersect = self.cursor.fetchall()
		#调用m1的方法集合 union 调用m2的方法集合
        sql = 'select callMethodname from methodinvocationinfo where calledmethodName = "%s" union select callMethodname from methodinvocationinfo where calledmethodName = "%s" ' % (m1, m2)
        self.execute(sql)
        callunion = self.cursor.fetchall()
		#被m1调用的方法 union 被m2调用的方法集合
        sql = 'select calledMethodname from methodinvocationinfo where callmethodName = "%s" union select calledMethodname from methodinvocationinfo where callmethodName = "%s" ' % (m1, m2)
        self.execute(sql)
        calledunion = self.cursor.fetchall()
        #被m1访问的成员变量 union 被m2 访问的成员变量集合
        sql = 'select name from variableinfo where  isField = 1 and belongedMethod = "%s" union select name from variableinfo where isField = 1 and belongedMethod = "%s"' % (m1, m2)
        self.execute(sql)
        accessunion = self.cursor.fetchall()
        return ( len(callintersect) + len(calledintersect) + len(accessintersect)) / ( len(callunion) + len(calledunion) + len(accessunion))
'''


