## This file uses training data to train a SVM classifier

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
from sklearn.svm import SVR
import pickle



def load_w2v_nor(sample_data,classes,f):
    sample_data=sample_data.sample(frac=1)
    folds=dict()
    ct=0
    size=len(sample_data)
    yy=collections.Counter(list(sample_data.iloc[:,-1]))
    yy
    N=min(yy.values())
    for cc in range(f):
        folds[cc]=[[],[],[]] 
        for c in range(len(classes)):
            temp_df=sample_data.loc[sample_data['class_code']==c]
            start_i=cc*(N//f)
            end_i=(cc+1)*(N//f)
            ind_lst=[list(temp_df.index)[i] for i in range(start_i,end_i)]
            for ii in range(start_i,end_i):
                #print(temp_df.iloc[ii,-2])
                if type(temp_df.iloc[ii,11])==str: # anti/neutral/pro
                    temp=np.asarray([int(i) for i in temp_df.iloc[ii,11].split(',')])
                    if sum(temp)>0:
                        temp=list(temp/sum(temp))
                else:
                    temp=[0,0,0]
                    #continue
                
                if type(temp_df.iloc[ii,7])==str: #retweet
                    temp2=np.asarray([int(i) for i in temp_df.iloc[ii,7].split(',')])#[:5]
                    if sum(temp2)>0:
                        temp2=list(temp2/sum(temp2))
                else:
                    temp2=[0,0,0,0,0]
                    #continue
                    
                if type(temp_df.iloc[ii,12])==str:
                    temp3=np.asarray([int(i) for i in temp_df.iloc[ii,12].split(',')])
                    if sum(temp3)>0:
                        temp3=list(temp3/sum(temp3))
                else:
                    temp3=[0,0,0]
                    
                folds[cc][1]+=[list([float(n) for n in temp_df.iloc[ii,2].split(',')])+list(temp)+list(temp2)] #+list(temp)+list(temp2)
                #folds[cc][1]+=[list(temp)]
                folds[cc][0]+=[ind_lst[ii-start_i]]
                folds[cc][2]+=[class_code[temp_df.iloc[ii,0]]]
    return folds

def main():
    # read sample file: the file contains "class","w2v_nor","1-gram","2-gram","3-gram","retweet" columns
    sample_data=pd.read_csv("file_path",index_col=0)
    classes=['anti',  'neutral', 'pro'] #'unsure',
    class_code={'anti': 0, 'unsure': 1, 'neutral': 1, 'pro': 2}
    sample_data.loc[list(sample_data.index)[0],'class_code']=0
    sample_data.loc[:,'class_code']=[class_code[i] for i in sample_data.loc[:,'class']]
    #sample_data.sample(frac=1)
    sample_data=sample_data.sample(frac=1)
    #sample_data=sample_data.iloc[:,:]
    sample_data
  
    # Training to get best C and gamma, training,testing,cv data
    C_lst=[10**int(i) for i in list(np.arange(-5,5,1))]
    columns=['C','kernel','fold','Threshold','Classification','precision','recall','F1']
    result_df=pd.DataFrame(columns=columns)
    ind=0
    
    Threshold=0
    
    F=5 # 5 folds
    folds=load_w2v_nor(sample_data,classes,F)
    
    for f in range(F):
        print('fold=',f)
        x_train=list()
        y_train=list()
        id_train=list()
    
        x_test=list()
        y_test=list()
        id_test=list()
    
        for ff in range(F):
            if ff==f:
                id_test+=folds[ff][0]
                x_test+=folds[ff][1]
                y_test+=folds[ff][2]
            else:
                id_train+=folds[ff][0]
                x_train+=folds[ff][1]
                y_train+=folds[ff][2]
        for C in C_lst:
            for kernel in ['rbf','linear','sigmoid','poly','linear']:
                print('---------------------------------------------------')
                print("C=",C,"kernel=",kernel,'Threshold=',Threshold)
                #result_df.loc[ind,"C"],result_df.loc[ind,"kernel"]=C,kernel
                #FORE=np.reshape(np.zeros(len(y_cv)*len(emo_cat)),(len(emo_cat),len(y_cv)))
                    
                predict_df=pd.DataFrame(index=id_test,columns=['y_observe','y_predict'])
                predict_df.loc[:,'y_observe']=y_test
    
                for cc in range(len(classes)):
                    y_train2=[int(yi==cc) for yi in y_train]
                    
                    svr = SVR(kernel=kernel, C=C, gamma='scale',degree=2,max_iter=10000)
                    model=svr.fit(x_train, y_train2)
                    pickle.dump(model, open("add file path"+kernel
                                    +"_c"+str(cc)+"_f"+str(f)+'_test.sav', 'wb'))
                    
                    fore0=(model.predict(x_test))
                    fore0=[i if i>Threshold else 0 for i in fore0]
                    
                    predict_df.loc[:,cc]=fore0
                predict_df.loc[:,'y_predict']=[list(predict_df.iloc[iii,2:6]).index(max(list(predict_df.iloc[iii,2:6]))) if max(list(predict_df.iloc[iii,2:6]))>0 else 9 for iii in range(len(predict_df))]
                predict_df2=predict_df.loc[predict_df["y_predict"]!=9]
                report=classification_report(list(predict_df.iloc[:,0]), list(predict_df.iloc[:,1]),output_dict=True)
                print('-------------------------------------------')
                
                # save to summary table
                result_df.loc[ind,:]=[C,kernel,f,Threshold,'all']+list(report['weighted avg'].values())[:3]
                result_df.loc[ind+1,:]=[C,kernel,f,Threshold,'0']+list(report['0'].values())[:3]
                result_df.loc[ind+2,:]=[C,kernel,f,Threshold,'1']+list(report['1'].values())[:3]
                result_df.loc[ind+3,:]=[C,kernel,f,Threshold,'2']+list(report['2'].values())[:3]
                ind+=5

if __name__ == "__main__":
    main()
