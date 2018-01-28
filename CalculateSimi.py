#coding=utf-8
import  numpy as np
import operator
import re
from Dataset import *
from TFIDFAlg import *
from Util import *
import datetime


class CalculateSimilary:

    def __init__(self):
        self.ds = Dataset()
        self.allMethods = self.ds.getAllMethod()
        contents = []
        for method in self.allMethods:
            contents.append(method.content)
        self.tfidf = TFIDFAlg(contents)

    def simiDependence(self,m1,m2):

        dist = self.ds.simiDist(m1,m2)
        context = self.ds.simiContext(m1,m2)
        return np.maximum(dist,context )

    #计算语义相似度
    def simiLexical(self, m1, m2):
        index1 = self.ds.getMethodIndex(m1)
        index2 = self.ds.getMethodIndex(m2)
        sims = self.tfidf.simiarity(self.allMethods[index1].content)
        return sims[index2]


    #计算位置相似度
    def simiLocation(self, m1, m2):
        cut = re.compile('\(.*?\)') #删除小括号及其内容
        n1 = cut.sub('',m1)
        n2 = cut.sub('',m2)
        c1 = re.split('\.',n1)[0:-1]  #按照\.分割成各个字符以确定父类和其子类
        c2 = re.split('\.',n2)[0:-1]
        if c1[0] != c2[0]: return 0
        a = list((set(c1).union(set(c2)))^(set(c1)^set(c2)))    #获取a，即c1,c2的差集，方便后续确定两者距离
        la = len(a)             #a值
        maxlen = max( len(c1), len(c2))
        distance = maxlen - la
        sum = la/(la+distance)
        return sum

    #计算总体相似度
    def simi(self, m1, m2):
        begin = datetime.datetime.now()
        dependence = self.simiDependence(m1, m2)
        begin = showDuration(begin, "dependence")
        lexical = self.simiLexical(m1, m2)
        begin = showDuration(begin, "lexical")
        location = self.simiLocation(m1, m2)
        begin = showDuration(begin, "location")
        #if (dependence + lexical + location ) / 3 > 1:
        #print("dependence: %f, lexical：%f, location: %f " % (dependence,lexical, location ))
        return location, dependence, lexical, (dependence + lexical + location ) / 3

    collection = {}

    #计算项目中各方法与某一特定方法的相似度

    def simiValue(self, m, M, flag = -1):
        for method in M:
            self.collection[method] = self.collection[method] + flag * self.simi(m, method)

    #计算项目中各方法与偏好集合的相似度，偏好集合包括了用户喜好以及厌恶的方法
    def simiValue(self):
        allMethods = self.getAllMethod()
        for method in self.getLikingList():
            self.simiValue(method, allMethods, flag =1)
        for method in self.getDisLikingList():
            self.simiValue(method, allMethods, flag =-1)

    def recommend(self, count = 100):
        self.collection = {'a':31, 'bc':5, 'c':3, 'asd':4, 'aa':74, 'd':0}
        self.collection['werq'] = 5
        self.collection = sorted(self.collection.items(), key=operator.itemgetter(1), reverse=True)


    def score(self):
        print(self.collection)
        keys = self.collection.items()



