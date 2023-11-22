## This file processes raw text data to extract w2v features and dictionary features to make a tweet vector used for inputting into SVM classifier.

import time
import json
from time import sleep
import pymysql
import random
import numpy as np
import datetime
from tqdm import tqdm
from datetime import datetime, timedelta
import re
import sys
from scipy.stats.stats import pearsonr
from scipy import stats
import scipy
import pymysql
import re
import numpy as np
import matplotlib.pyplot as plt
import datetime
import collections
import MeCab
import requests
import ipadic
import time
import json
from time import sleep
import re
import sys
import emoji
import gensim
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import pandas as pd
import numpy as np
import pickle



def split(txt):
    word_prop=['名詞' ,'動詞',  '形容詞', '副詞' ,'感動詞', 'フィラー']
    for r in re.findall('@\S*',txt):#range(len(re.findall('@\S*',txt))):
        #txt=re.findall('@\S*\s(.*)',txt)[0]
        txt=txt.replace(r,'')
        
    hashtags=re.findall('(#\S*)',txt)
    for r in re.findall('(#\S*)',txt):
        txt=txt.replace(r,'')
        
    tagger=MeCab.Tagger("## please add mecab-ipadic-neologd file path")
    node=tagger.parseToNode(txt)
    word_lst=list()
    
    while node:
        word = node.surface
        pos = node.feature.split(",")[0]
        node = node.next
        
        if pos in ['記号','BOS/EOS','助動詞', '助詞','接頭詞', '連体詞', '接続詞','フィラー']:
            continue
        word_lst.append(word)
    return word_lst

def word_SVM(vocabulary):
    try:
        v1=np.asarray(model_hottolink.get_vector(vocabulary[0]))
    except:
        v1=np.zeros(200)
    w2v_mat=np.asarray([v1])

    for i in range(1,len(vocabulary)):
        print(i,end='\r')
        try:
            v1=np.asarray(model_hottolink.get_vector(vocabulary[i]))
            #v1=v1/np.sqrt(sum(v1**2))
        except:
            v1=np.zeros(200)
        #np.vstack([w2v_mat,v1])
        w2v_mat=np.append(w2v_mat,[v1],axis=0)
    return w2v_mat

def get_hash(txt):
    hashtags=re.findall('(#\S*)',txt)
    return hashtags
    
def find_SVM(txt):  
    word_prop=['名詞' ,'動詞',  '形容詞', '副詞' ,'感動詞', 'フィラー']
    #print(txt)
    for r in re.findall('@\S*',txt):#range(len(re.findall('@\S*',txt))):
        #txt=re.findall('@\S*\s(.*)',txt)[0]
        txt=txt.replace(r,'')
        
    url=re.findall('(http\S*)',txt)
    for r in re.findall('(http\S*)',txt):
        #txt=re.findall('(http.*\s)',txt)[0]
        txt=txt.replace(r,'')
    #print(txt)
    tagger=MeCab.Tagger("## please add mecab-ipadic-neologd file path")
    #ipadic.MECAB_ARGS,unidic-csj
    node=tagger.parseToNode(txt)
    #temp_v=np.zeros(200)
    w2v_mat=[]
    ct=0
    
    temp_dict=dict()
    word_dict=dict()
    word_lst=list()
    temp_v=np.zeros(200)
    
    for tt in word_prop:
        temp_dict[tt]=np.zeros(200)
    
    while node:
        word = node.surface
        pos = node.feature.split(",")[0]
        node = node.next
        if pos in ['記号','BOS/EOS','助動詞', '助詞','接頭詞', '連体詞', '接続詞','フィラー'] or word.encode().isalpha():
            continue
        
        if pos not in word_dict.keys():
            word_dict[pos]=list()
        word_dict[pos].append(word)
        
        try:
            v1=model_hottolink.get_vector(word)
            temp_v+=list(v1)
            word_lst.append(word)
        except:
            continue
    
    return w2v_mat,word_lst

    
def SVM_nor(v,threshold):
    kernel='rbf'
    result_lst=list()
    for f in range(5):
        # load 5 folds SVM classifier
        model1=pickle.load(open("add SVM model 1 path", 'rb'))
        pre1=model1.predict(v)
        model2=pickle.load(open("add SVM model 2 path", 'rb'))
        pre2=model2.predict(v)
        model3=pickle.load(open("add SVM model 3 path", 'rb'))
        pre3=model3.predict(v)
        model4=pickle.load(open("add SVM model 4 path", 'rb'))
        pre4=model4.predict(v)
        #model5=pickle.load(open("add SVM model 5 path", 'rb'))
        pre5=model5.predict(v)
        predict0=[pre1[0],pre2[0],pre3[0],pre4[0]]#,pre5[0]]
        if max(predict0)<=threshold:
            result='no result'
            result_lst.append(9)
        else:
            result=predict0.index(max(predict0))
            result_lst.append(result)
    return result_lst


def n_gram(txt,n):
    n_g=list()
    tagger=MeCab.Tagger("## please add mecab-ipadic-neologd file path")
    node=tagger.parseToNode(txt)
    word_lst=list()
    while node:
        word = node.surface
        pos = node.feature.split(",")[0]
        node = node.next
        if pos in ['記号','BOS/EOS','助動詞', '助詞','接頭詞', '連体詞', '接続詞','フィラー'] or word.encode().isalpha() or word.isnumeric() or len(word)<2: #,'助動詞', '助詞','接頭詞', '連体詞', '接続詞','フィラー'] or         'next'
            'next'
        else:
            word_lst.append(word)
    for i in range(len(word_lst)-n+1):
        n_g.append('-'.join(word_lst[i:i+n]))
    n_g=list(set(list(n_g)))
    return n_g

def main():
    
    # load hottolink database
    model_hottolink = KeyedVectors.load_word2vec_format(file_w2v_hottolink, binary=False)
    
    # load sample data:
    sample_data=pd.read_csv("add path")
    w2v_mat=[]
    for s in range(len(sample_data)):
        print(s,end='\r')
        txt=sample_data.iloc[s,"???"]
        w2v,word_lst=find_SVM(txt)
        if len(word_lst)>0:
            #print(word_lst)
            #tfidf=find_tdidf(word_lst)
            w2v_v=np.sum(w2v,axis=0)
            ind=list(sample_data.index)[s]
            if s==0:
                w2v_mat=np.asarray(list(w2v_v))
            else:
                w2v_mat=np.vstack((w2v_mat,w2v_v))
            sample_data.loc[ind,'1-gram']=','.join(n_gram(txt,1))
            sample_data.loc[ind,'2-gram']=','.join(n_gram(txt,2))
            sample_data.loc[ind,'3-gram']=','.join(n_gram(txt,3))
            sample_data.loc[ind,'hashtags']=','.join(get_hash(txt))
            
    sample_data.loc[:,'w2v_nor']=[','.join([str(round(ii,2)) for ii in i]) for i in (w2v_mat-np.average(w2v_mat,axis=0))/np.std(w2v_mat,axis=0)]

if __name__ == "__main__":
    main()
