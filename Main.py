from Dataset import  *

from CalculateSimi import *

ds = Dataset()
#methods = ds.getAllMethod()

method1 = "com.microstar.xml.HandlerBase.endDocument()"
method2 = "com.microstar.xml.HandlerBase.charData(char[],int,int)"


similary =CalculateSimilary()
#print(similary.simiLocation(method1,method2))
#print(similary.simiLexical( method2, method2))
methods = ds.getAllMethod()
documents = []
for method in methods:
    documents.append(method.content)
tfidf = TFIDFAlg(documents)
#print(methods)
#sort_sims = tfidf.simiarity("China supports DPRK, ROK in fostering trust, building consensus through dialogue")
#print(sort_sims)
#tfidf.otherTFIDF(documents, documents[3])
print(tfidf.simiarity(documents[2]))
print("************************")
print(tfidf.sortedSimiarity(documents[2]))



