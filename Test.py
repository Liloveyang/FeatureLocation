import sqlite3
import numpy as np
from CalculateSimi import *

#一些额外的操作，例如将父类中的方法加入到子类中，但在本次实现中没用调用
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



s = set()
s.add(5)
s.add(6)
t = set()
t.add(5)
s = s.difference(t)
print (s)


'''
ds = Dataset()
goldsets = ds.getGoldSets()
counts = []
for goldset in goldsets:
    methods = goldset.methods[:-1].split("\n")
    counts.append(len(methods))
print("mean: %f, average: %f, max: %d, sum :%d" % (np.mean(counts), np.average(counts), np.max(counts), np.sum(counts)))
'''
