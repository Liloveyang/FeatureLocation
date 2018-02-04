from Dataset import *
from CalculateSimi import *

#用于生成推荐结果
class Recommend:

    def __init__(self):
        self.RecommendNum = 20
        self.ds = Dataset()

    # 从候选方法列表中，删除被加入到like或disklike的方法。
    def removeselectedMethods(self, condidateMethods, likelist, dislikelist):
        for method in likelist:
            for condidate in condidateMethods:
                if condidate[0] == method:
                    condidateMethods.remove(condidate)
                    break
        for method in dislikelist:
            for condidate in condidateMethods:
                if condidate[0] == method:
                    condidateMethods.remove(condidate)
                    break

    def evaluaterecommendquality(self, recommendmethods, ID, rounds, likelist):
        goldsets = self.ds.getGoldSets()
        for goldset in goldsets:
            if goldset.ID == ID:
                methodset = set()
                for method in goldset.methods[:-1].split("\n"):
                    methodset.add(method)
                methodset = methodset.difference(set(likelist))
                locations = ""
                count = 0
                for ind, method in enumerate(recommendmethods):
                    if method[0] in methodset:
                        locations = locations + str(ind) + ","
                        count +=1
                recall = count / len(methodset)
                sql = "insert into recommendation (ID, hitcount, rounds, hitlocation, recall ) " \
                      "values('%s', %d, %d ,'%s', %f)" % (ID, count, rounds, locations, recall)
                self.ds.executeupdate(sql)

    #综合考虑like和dislike与候选方法的相关度，并根据投票进行推荐
    def recommandResult(self):

        entrancepoints = self.ds.getEntrancePoint()
        methods = self.ds.getAllMethodName()
        calculator = CalculateSimilary()
        self.ds.executeupdate("delete from recommendation")
        for entrancepoint in entrancepoints: #为每个任务寻找答案
            #持续时间太长，每做完一个任务就保存一次
            recommendresult =[]
            index = entrancepoints.index(entrancepoint)
            begin = datetime.datetime.now()
            print("start: " , (index, entrancepoint.ID,begin ))
            likelist = entrancepoint.methods.split("\n") # 对于每个任务，已加入到like的方法列表。初始状态下，likelist仅包含entrance points
            rounds = 0

            for method in likelist:
                result = RecommendResult(entrancepoint.ID, rounds)
                result.methodName = method
                result.islike = True
                rounds +=1
                recommendresult.append(result)
            dislikelist = []

            while len(likelist) < 10:
                rounds += 1
                print("%d/10: " % len(likelist))
                likerecommendmethods, like_loc, like_dep, like_lex = self.recommend(likelist, calculator, methods)
                 # 对于各个任务，从推荐列表中删除已被加入到like或dislike的方法
                self.removeselectedMethods(likerecommendmethods, likelist, dislikelist)
                # 对每次迭代得到的推荐列表进行评价，查看其准确率
                self.evaluaterecommendquality(likerecommendmethods, entrancepoint.ID, rounds, likelist )
                recommendmethods =[]
                result = RecommendResult(entrancepoint.ID, rounds)
                if len(dislikelist) > 0:
                    dislikerecommend, dislike_loc, dislike_dep, dislike_lex = self.recommend(dislikelist, calculator, methods)
                    for recmethod in likerecommendmethods:
                        vote = 0
                        methodname = recmethod[0]
                        if like_loc[methodname] > dislike_loc[methodname] : vote +=1
                        if like_dep[methodname] > dislike_dep[methodname] : vote +=1
                        if  like_lex[methodname] > dislike_lex[methodname] : vote +=1
                        if vote > 0 : recommendmethods.append(recmethod)
                        if len(recommendmethods) >= self.RecommendNum : break;
                else:
                    recommendmethods = likerecommendmethods[:self.RecommendNum]
                randnum = random.uniform(0,1)
                dic = dict(recommendmethods)
                if randnum <= 0.8:
                    ind, value = wheelselection(dic.values())
                    selectedmethod, simi = recommendmethods[ind]
                    likelist.append(selectedmethod)
                    result.islike = True
                    result.methodName = selectedmethod
                else:
                    ind, value = reversewheelselection(dic.values())
                    selectedmethod, simi = recommendmethods[ind]
                    dislikelist.append(selectedmethod)
                    result.islike = False
                    result.methodName = selectedmethod
                recommendresult.append(result)
            self.ds.saverecommendresult(recommendresult)
            print("completed: " , (index, entrancepoint.ID,datetime.datetime.now() - begin ))

    #只考虑entrancepoint，不再模拟用户操作。
    def recommandResultOneShot(self):

        entrancepoints = self.ds.getEntrancePoint()
        methods = self.ds.getAllMethodName()
        calculator = CalculateSimilary()
        self.ds.executeupdate("delete from recommendation")
        rounds = 0
        for entrancepoint in entrancepoints: #为每个任务寻找答案
            #持续时间太长，每做完一个任务就保存一次
            rounds +=1

            recommendresult =[]
            index = entrancepoints.index(entrancepoint)
            print("%d/%d" % (index, len(entrancepoints) ))
            begin = datetime.datetime.now()
            print("start: " , (index, entrancepoint.ID,begin ))
            likelist = entrancepoint.methods.split("\n") # 对于每个任务，已加入到like的方法列表。初始状态下，likelist仅包含entrance points
            for method in likelist:
                result = RecommendResult(entrancepoint.ID, rounds)
                result.methodName = method
                result.islike = True
                recommendresult.append(result)
            dislikelist = []
            likerecommendmethods, like_loc, like_dep, like_lex = self.recommend(likelist, calculator, methods)
             # 对于各个任务，从推荐列表中删除已被加入到like或dislike的方法
            self.removeselectedMethods(likerecommendmethods, likelist, dislikelist)
            # 对每次迭代得到的推荐列表进行评价，查看其准确率
            self.evaluaterecommendquality(likerecommendmethods, entrancepoint.ID, rounds, likelist )
            recommendresult.append(result)
            self.ds.saverecommendresult(recommendresult)
            print("completed: " , (index, entrancepoint.ID,datetime.datetime.now() - begin ))



    #推荐与选定方法集合相关度最高的N个方法
    def recommend(self, selectedMethods, calculator, condidateMethods, N = 200):
        dic_r = {}
        dic_loc = {}
        dic_dep = {}
        dic_lex = {}
        for method in condidateMethods:
            dic_r[method] = 0  # 组合相关度
            dic_loc[method] = 0  # 位置相关度
            dic_dep[method] = 0  # 依赖相关度
            dic_lex[method] = 0  # 内容相关度
        for singleMethod in selectedMethods:  # 为每个like或dislike计算其他方法与它的相似度
            for method in condidateMethods:
                loc, dep, lex, r = calculator.simi(singleMethod, method)
                dic_r[method] += r
                dic_loc[method] += loc
                dic_dep[method] += dep
                dic_lex[method] += lex
        for item in dic_r:
            dic_r[item] /=  len(selectedMethods)
        sorted_dic = sorted(dic_r.items(), key=lambda item: -item[1])
        return sorted_dic[:N], dic_loc, dic_dep, dic_lex


