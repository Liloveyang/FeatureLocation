import numpy as np
import string
from Dataset import *
import re
import sqlite3
from CalculateSimi import *

def getSimpleName(methodname):
    index = methodname.find("(")
    str = methodname[0: index]
    leftindex = str.rfind('.')
    return methodname[leftindex+1:]


# 将父类中的方法继承到子类中，需考虑1.子类重写父类的方法；2.多级继承
def inheritParent():
    ds = Dataset()
    ds.execute("delete from methodinfo where ismanual = 1")
    ds.commit()
    sqlresult = ds.execute("select name from classinfo where superclass not in ( select name from classinfo ) and name like '%TextArea'order by superclass")
    allSuperClasses =  sqlresult.fetchall()
    for _class in allSuperClasses:
        enrichChild(_class[0], ds)

# 将方法加入到子类中，className为子类的类名，methods是父类中的方法， 当子类已存在与父类中同名的方法时，保留子类中的该方法，否则继承父类中的方法
def addMethodIntoChild(className, methods, ds):
    for method in methods:
        sqlresult = ds.execute("select * from methodinfo where className ='%s' and name ='%s'" % (className, method[1]))
        if len( sqlresult.fetchall()) >0 :
            continue
        newMethod = getSimpleName(method[1])
        newMethod = className + "." + newMethod
        content = re.subn(r'\'' , ' ', method[8])[0]
        javadoc = re.subn(r'\'' , ' ', method[2])[0]
        sql = "insert into methodinfo (projectname, name, javadoc, classname, returntype, modifies, throwexceptions, isConstructor, content, isManual) " \
              "values ('%s', '%s', '%s','%s','%s', '%s', '%s', '%s','%s', 1)" % (method[0], newMethod, javadoc, className, method[4], method[5], method[6], method[7], content)
        try:
            ds.execute(sql)
        except sqlite3.OperationalError:
            print(sql)
        ds.commit()

def enrichChild(superClass, ds):
    sqlresult = ds.execute("select * from methodinfo where modifies not like '%private%' and classname ='" + superClass +"'"  )
    methodinSuperClass = sqlresult.fetchall()
    children = ds.execute("select name from classinfo where superclass = '%s'" % superClass)
    for child in children.fetchall():
        addMethodIntoChild(child[0], methodinSuperClass, ds)
        enrichChild(child[0], ds)


#inheritParent()

def recommandResult():
    ds = Dataset()
#    sql = 'delete from recommandResult'
#    ds.execute(sql)
#    ds.commit()
    entrancepoints = ds.getEntrancePoint()
    methods = ds.getAllMethod()
    calculator = CalculateSimilary()

    dic ={}
    for method in methods:
        dic[method.name] = 0
    for entrancepoint in entrancepoints: #为每个任务寻找答案
        begin = datetime.datetime.now()
        allMethods = entrancepoint.methods.split("\n") #得到每个任务的入口
        for singleMethod in allMethods :               #为每个入口计算其他方法与它的相似度
            for method in methods:
                dic[method.name] +=  calculator.simi(singleMethod, method.name)
        for item in dic:
            dic[item] /= len(allMethods)
            print("%s : %f" % (item, dic[item]))
        showDuration(begin,"task %d" % len(allMethods))
        break



'''
    content = []
    sqlInsert = "insert into recommandResult( methods , result ) values (? , ?)"
    cal = CalculateSimilary
    for i in range(0 , len(methods)):
        for m2 in methods:
            result = cal.simi(m1,m2)
            content.append( m2 , result)
    ds.executemany( sqlInsert , content)
    ds.commit()
    sqlReco = 'select methods from recommandResult order by result desc where rowid <= 50'
    reco = ds.execute()
    return reco.fetchall()
'''
#recommandResult()




