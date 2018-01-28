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
 # currentmethods列表中，删除被加入到like或disklike的方法。
def removeselectedMethods(currentmethods, likelist, dislikelist):
    for method in likelist:
        if currentmethods.count(method)>0:
            currentmethods.remove(method)
    for method in dislikelist:
        if currentmethods.count(method)>0:
            currentmethods.remove(method)

def recommandResult():
    ds = Dataset()
#    sql = 'delete from recommandResult'
#    ds.execute(sql)
#    ds.commit()
    entrancepoints = ds.getEntrancePoint()
    methods = ds.getAllMethodName()
    calculator = CalculateSimilary()


    ignored = []
    for entrancepoint in entrancepoints: #为每个任务寻找答案
        # 对于各个任务，都需要从methods列表中删除被加入到like和dislike列表的方法，因此创建一个临时的currentAllmethods来保存
        currentmethods = methods.copy()
        index = entrancepoints.index(entrancepoint)
        print("%d %s", (index, entrancepoint.ID))
        if  index in ignored:
            continue
        likelist = entrancepoint.methods.split("\n") # 对于每个任务，已加入到like的方法列表。初始状态下，likelist仅包含entrance points
        dislikelist = []
        while len(likelist) < 10:
            removeselectedMethods(currentmethods, likelist, dislikelist)
            likerecommendmethods, like_loc, like_dep, like_lex = recommend(likelist, calculator, methods)
            recommendmethods =[]
            if len(dislikelist) > 0:
                dislikerecommend, dislike_loc, dislike_dep, dislike_lex = recommend(dislikelist, calculator, methods)
                for recmethod in likerecommendmethods:
                    vote = 0
                    methodname = recmethod[0]
                    if like_loc[methodname] > dislike_loc[methodname] : vote +=1
                    if like_dep[methodname] > dislike_dep[methodname] : vote +=1
                    if  like_lex[methodname] > dislike_lex[methodname] : vote +=1
                    if vote > 0 : recommendmethods.append(recmethod)
                    if len(recommendmethods) >= 50 : break;
            else:
                recommendmethods = likerecommendmethods[:50]

            randnum = random.uniform(0,1)
            dic = dict(recommendmethods)
            print("count: %d" % len(recommendmethods))
            if randnum <= 0.8:
                ind, value = wheelselection(dic.values())
                selectedmethod, simi = recommendmethods[ind]
                likelist.append(selectedmethod)
                print("likelist: " )
                print(likelist)
            else:
                ind, value = reversewheelselection(dic.values())
                selectedmethod, simi = recommendmethods[ind]
                dislikelist.append(selectedmethod)
                print("dislikelist: " )
                print(dislikelist)
        break


def recommend(allMethods, calculator, methods,  N = 200):
    dic_r = {}
    dic_loc = {}
    dic_dep = {}
    dic_lex = {}
    for method in methods:
        dic_r[method] = 0  # 组合相关度
        dic_loc[method] = 0  # 位置相关度
        dic_dep[method] = 0  # 依赖相关度
        dic_lex[method] = 0  # 内容相关度
    for singleMethod in allMethods:  # 为每个like或dislike计算其他方法与它的相似度
        for method in methods:
            loc, dep, lex, r = calculator.simi(singleMethod, method)
            dic_r[method] += r
            dic_loc[method] += loc
            dic_dep[method] += dep
            dic_lex[method] += lex
    for item in dic_r:
        dic_r[item] /=  len(allMethods)
    sorted_dic = sorted(dic_r.items(), key=lambda item: -item[1])
    return sorted_dic[:N], dic_loc, dic_dep, dic_lex


recommandResult()




