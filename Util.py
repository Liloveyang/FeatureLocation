# coding:utf-8
import re
import numpy as np
import random
import timeit
Infinite = 1000000

# 轮盘的逆操作，fitness越大被选中的概率越低
def reversewheelselection(fitness):
    fitness = list(fitness)
    maxfitness = max(fitness)
    newvalue = fitness
    for ind, val in enumerate(newvalue):
         newvalue[ind] = maxfitness - val
    return wheelselection(newvalue)



"""
Basic roulette wheel selection: O(N)
"""
def wheelselection(fitness):
    '''
    Input: a list of N fitness values (list or tuple)
    Output: selected index
    author: Created on Mon Feb 29, 2016
    @author: mangwang
    @source: https://github.com/mangwang/PythonForFun/blob/master/rouletteWheelSelection.py
    '''
    sumFits = sum(fitness)
    # generate a random number
    rndPoint = random.uniform(0, sumFits)
    # calculate the index: O(N)
    accumulator = 0.0
    for ind, val in enumerate(fitness):
        accumulator += val
        if accumulator >= rndPoint:
            return ind, val


def showDuration(begin, name):
    end = timeit.default_timer()
    #print("%s: %s" % (name, str(end - begin)))
    return timeit.default_timer()

def tokenization(content):
    result = []
    content = re.subn(r'[\W]' , ' ', content)[0].lower()
    for word in content.split():
        result.append(word)
    return result


def infiniteMatrix(shape):
    result = np.ones(shape)
    for i in range(0,result.shape[0]):
        for j in range(0,result.shape[1]):
            result[i][j] = Infinite
    return result

#matrix = np.mat([[0,1,100,4],[100,0,9,2],[3,5,0,8],[100,100,6,0]])

def folyd(A):
    v_len = A.shape[0]
    for a in range(v_len):
        print("%d / %d" % (a, v_len ))
        for b in range(v_len):
            for c in range(v_len):
                if(A[b,a]+A[a,c]<A[b,c]):
                    A[b,c] = A[b,a]+A[a,c]
    return A

#Folyd(matrix)
''' Floyd 优化
void Floyd_4(){
    for(int k = 1; k <= N; k++){
        for(int i = 1; i <= N; i++){
            if(k != i){
                int t = (k<i) ? A[i][k] : A[k][i];
                if(t == Inf)  continue;
                for(int j = 1; j <= ((k<i)?k:i); j++){
                    if(t+A[k][j] < A[i][j])  A[i][j] = t + A[k][j];
                }
                for(int j = k+1; j <= i; j++){
                    if(t+A[j][k] < A[i][j])  A[i][j] = t + A[j][k];
                }
            }
        }
    }
    return ;
}
'''
