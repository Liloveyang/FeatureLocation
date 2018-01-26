#coding=utf-8

from gensim import corpora, models, similarities
from Util import tokenization


class TFIDFAlg:

    def __init__(self, corpora_documents):
        # 生成字典和向量语料
        result = []
        for sentence in corpora_documents:
            result.append( tokenization(sentence))
        self.dictionary = corpora.Dictionary(result)
        # print(dictionary)
        # dictionary.save('dict.txt') #保存生成的词典
        # dictionary=Dictionary.load('dict.txt')#加载

        # 通过下面一句得到语料中每一篇文档对应的稀疏向量（这里是bow向量）
        corpus = [self.dictionary.doc2bow(text) for text in result]
        # 向量的每一个元素代表了一个word在这篇文档中出现的次数
        # print(corpus)
        # corpora.MmCorpus.serialize('corpuse.mm',corpus)#保存生成的语料
        # corpus=corpora.MmCorpus('corpuse.mm')#加载

        # corpus是一个返回bow向量的迭代器。下面代码将完成对corpus中出现的每一个特征的IDF值的统计工作
        self.tfidf_model = models.TfidfModel(corpus)
        corpus_tfidf = self.tfidf_model[corpus]
        self.similarity = similarities.Similarity('Similarity-tfidf-index', corpus_tfidf, num_features=len(self.dictionary))

    def simiarity(self, query ):
        test_corpus_1 = self.dictionary.doc2bow(tokenization(query))  #
        test_corpus_tfidf_1 = self.tfidf_model[test_corpus_1]  # 根据之前训练生成的model，生成query的IFIDF值，然后进行相似度计算
        # [(51, 0.7071067811865475), (59, 0.7071067811865475)]
        result = self.similarity[test_corpus_tfidf_1]
        return result

    def sortedSimiarity(self, query):
        result = self.simiarity(query)
        sort_sims = sorted(enumerate(result), key = lambda item:-item[1])
        return sort_sims



