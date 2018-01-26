# coding:utf-8
import re
import numpy as np
import datetime
Infinite = 1000000

def showDuration(begin, name):
    end = datetime.datetime.now()
    print("%s: %s" % (name, str(end - begin)))
    return datetime.datetime.now()

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
