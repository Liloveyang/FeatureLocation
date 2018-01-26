from Dataset import *
import numpy as np
import sqlite3 as sql
import random
import os
from Util import *

# 创建不同方法的调用距离表
def createdistanInvocate():
    ds = Dataset()
    methods = ds.getAllInvocateMethod()
    matrix = infiniteMatrix((len(methods), len(methods)) )
    r = []
    for method in methods:
        r.append(method[0])
    print("Create matrix")

    invocations = ds.getAllMethodInvocation()
    count1 = count2 =0
    for invocation in  invocations:
        indexCallMethod = r.index(invocation.callMethod)
        try:
            indexCalledMethod = r.index(invocation.calledMethod)
            matrix[indexCallMethod][indexCalledMethod] = 1
            count1 +=1
        except ValueError:
            count2 +=1
    print("count1: %d, count2: %d, sum: %d" % (count1, count2, count2+count1))
    #index = r.index("com.microstar.xml.HandlerBase.resolveEntity(java.lang.String,java.lang.String)")
    #print( index ) #输入方法名可得其编号
    #print(r[index]) #输入编号可得方法名
    print("Foldy")
    matrix = folyd(matrix)
    print("Insert datatable")
    content = []
    sql = "insert into simDistance( callMethodName, calledMethodName, length) values (?, ?, ?)"
    for i in range(0, matrix.shape[0]):
        callMethod = r[i]
        for j in range(0, matrix.shape[1]):
            if matrix[i][j] < Infinite :
                calledMethod = r[j]
                value = matrix[i][j]
                content.append((callMethod, calledMethod, value))
    ds.executemany(sql, content)
    ds.commit()
    print(len(content))

from Dataset import *
import re



def spliteParams(oriname):        #处理比对数据Y
    index = oriname.find("(")
    right = oriname[index+1: ]
    resY = re.split('[,<]',right)
    return resY

def transferSql(oriname):            #处理比对方法参数Y,插入%以便查找数据库
    index = oriname.find("(")
    left = oriname[0:index+1]
    right = oriname[index+1: ]
    content = ""
    for item in re.split('[,<]', right):
        content = content  + item + "%"
    return left + "%" + content + "'"

#将goldSets中的方法转换成能够与数据库中的匹配方法，如补充参数的完整类型名等，其中，会出现有些goldset中的方法在系统中不存在，坑爹的鬼
def createBenchmark():
    path = "resource/benchmark/GoldSets/"
    ds = Dataset()
    setResult = {}
    for file in os.listdir(path):
        with open(path + file, encoding='utf-8') as f:
            origiMethods = ""
            updatedMethods = ""
            for line in f:
                if line.find("\n") > 0 :
                    line = line[0:-1]
                resY = spliteParams(line)             #获得对比方法中参数

                origiMethods = origiMethods  + line + "\n"
                sql = "select name from methodinfo where name like '" + transferSql(line)
                sqlresult = ds.execute(sql)
                methods = sqlresult.fetchall()        #获得原方法中参数，以便后续对比
                if( len(methods) == 0):
                    print(line )    #找出匹配不上的方法

                for i in range(0,len(methods)):
                    resX = spliteParams(methods[i][0])
                    result = 1
                    if(len(resX) != len(resY)): #如果两个数据长度不同，即参数个数不等，直接结果错误
                         continue
                    for j in range(0,len(resX)):
                        if(resX[j].find(resY[j]) == -1):    #参数匹配则设为1
                            result = 0
                    if result == 1:                         #比对完全正确则插入数据库
                        updatedMethods = updatedMethods  + methods[i][0] + "\n"
                        break
            id = re.findall('\d+',file)                         #取出ID号
            ID = "".join(id)                                    #将list转换为字符串
            sql = "insert into goldSets(ID,methods, origiMethods) values ('%s','%s', '%s')" % (ID, updatedMethods, origiMethods)   #数据库未插入，原因未知？？？？？
            ds.execute(sql)
            ds.commit()
#createBenchmark()
def createEntrancePoint():
    ds = Dataset()
    goldsets = ds.getGoldSets()
    content = []
    sql = "delete from entrancePointInfo"
    ds.execute(sql)
    ds.commit()
    sql = "insert into entrancePointInfo( ID, methods) values (?, ?)"
    for goldset in goldsets:
        ID, methods = goldset.ID, goldset.methods
        methods = methods[: -1].split("\n")
        count = np.ceil( len(methods) /5 )
        slice = random.sample(methods, int(count))
        slice = "\n".join(slice)
        content.append((ID, slice))
    ds.executemany(sql, content)
    ds.commit()

#createEntrancePoint()
# 调用关系字典，key为(调用者，被调用者), value = 1
invocationDic = {}
# 直接调用关系字典， key为调用者, value 为所有被key调用的方法
invocatorDic = {}
def recuitInvocate(invocator, invocated, length):

    print("%s call %s, %d" %(invocator, invocated, length) )
    if length > 10: return
    length +=1
    if (invocator, invocated) in invocationDic.keys():
        if invocationDic[invocator, invocated] > length:
            invocationDic[invocator, invocated] = length
    else:
        invocationDic[invocator, invocated] = length
    if invocated in invocatorDic.keys():
        for nextInvocated in invocatorDic[invocated]:
            recuitInvocate(invocator, nextInvocated, length)


def createRecuitdistanInvocate():
    ds = Dataset()
    ds.execute("delete from simDistance")
    ds.commit()
    allInvocations = ds.getAllMethodInvocation()
    invocationDic ={}
    for invocation in allInvocations:
        invocationDic[invocation.callMethod, invocation.calledMethod] = 1
    ds.execute("select distinct(callmethodname) from methodinvocationinfo ")
    temp = ds.cursor.fetchall()
    invocators = []
    for item in temp:
        invocators.append(item[0])
    for invocator in invocators:
        invocatorDic[invocator] = []
    ds.execute("select callMethodName, calledMethodName from methodinvocationinfo")
    for invocation in ds.cursor.fetchall():
        invocation = MethodInovation(invocation)
        invocatorDic[invocation.callMethod].append(invocation.calledMethod)
    for invocator in invocators:
        for invocated in invocatorDic[invocator]:
            recuitInvocate(invocator, invocated, 1)
    content = []
    sql = "insert into simDistance( callMethodName, calledMethodName, length) values (?, ?, ?)"
    for key in invocationDic.keys():
        content.append((key[0], key[1], invocationDic[key]))
    ds.executemany(sql, content)
    ds.commit()
createRecuitdistanInvocate()

