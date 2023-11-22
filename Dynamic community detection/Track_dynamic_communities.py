import pandas as pd
import time
import json
from time import sleep
import random
import numpy as np
import datetime
from tqdm import tqdm
from datetime import datetime, timedelta
import re
import sys
from scipy.stats.stats import pearsonr
from scipy import stats
from scipy.stats.stats import pearsonr
from scipy import stats
import scipy
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns

def convert_jac_df(jac):
    
    jac_df=pd.DataFrame(index=list(dict.fromkeys(list(jac.iloc[:,0]))),columns=list(dict.fromkeys(list(jac.iloc[:,1]))))
    jac_df
    for j in range(len(jac)):
        jac_df.loc[jac.iloc[j,0],jac.iloc[j,1]]=jac.iloc[j,2]
    jac_df=jac_df.fillna(0)
    jac_df.loc[:,'total']=np.sum(np.asarray(jac_df.iloc[:,:]),axis=1)
    jac_df=jac_df.sort_values('total',ascending=False)
    jac_df=jac_df.iloc[:,:-1]
    jac_df.loc['total',:]=np.sum(np.asarray(jac_df.iloc[:,:]),axis=0)
    jac_df=jac_df.sort_values('total', axis=1,ascending=False)
    jac_df.loc[:,'total']=np.sum(np.asarray(jac_df.iloc[:,:]),axis=1)
    return jac_df

def pre_suc_generator(jac_df):
    sim_mat1=np.round(np.asarray(jac_df.iloc[:-1,:-1])/np.reshape(np.asarray(jac_df.iloc[:-1,-1]),(len(jac_df)-1,1)),1)
    sim_mat2=np.round(np.asarray(jac_df.iloc[:-1,:-1])/np.asarray(jac_df.iloc[-1,:-1]),1)

    pre_dict=pd.DataFrame(columns=['from','to','size','sim_score'])
    I,J=sim_mat1.shape
    iid=0

    thresh=0.1
    for i in range(I):
        if list(jac_df.index)[i]!=0:
            #temp=list(jac_df.iloc[i,:-1])
            #print(jac_df.iloc[i,:])
            #print(jac_df.iloc[i,-1])

            for j in range(len(jac_df.columns)-1):
                if jac_df.iloc[i,j]/jac_df.iloc[i,-1]>thresh and jac_df.iloc[-1,j]>=0.01 and list(jac_df.columns)[j]!=0 and jac_df.iloc[i,j]/jac_df.iloc[-1,-1]>=0.001:
                    #print(i,list(jac_df.index)[i])
                    #print('ID',j,',to_com',list(jac_df.columns)[j],',ratio_from_com',round(jac_df.iloc[i,j]/jac_df.iloc[i,-1],2),',size ratio of to_com',round(jac_df.iloc[-1,j],2))
                    #print('------')

                    pre_dict.loc[iid,:]=[list(jac_df.index)[i],list(jac_df.columns)[j],jac_df.iloc[i,j],round(jac_df.iloc[i,j]/jac_df.iloc[i,-1],2)]
                    iid+=1
            #print(pre_dict.loc[i,:])

    suc_dict=pd.DataFrame(columns=['from','to','size','sim_score'])
    I,J=sim_mat2.shape

    
    iid=0
    for j in range(J):
        if list(jac_df.columns)[j]!=0:
            temp=list(jac_df.iloc[:-1,j])

            for i in range(len(jac_df.index)-1):

                if jac_df.iloc[i,j]/jac_df.iloc[-1,j]>thresh and jac_df.iloc[i,-1]>=0.01 and list(jac_df.index)[i]!=0 and jac_df.iloc[i,j]>=0.01:
                    #print(j,list(jac_df.columns)[j])
                    #print('ID',i,',from_com',list(jac_df.index)[i],',ratio_to_com',round(jac_df.iloc[i,j]/jac_df.iloc[-1,j],2),',size ratio of from_com',round(jac_df.iloc[i,-1],2))
                    #print('------------------------')
                    suc_dict.loc[iid,:]=[list(jac_df.index)[i],list(jac_df.columns)[j],jac_df.iloc[i,j],round(jac_df.iloc[i,j]/jac_df.iloc[-1,j],2)]
                    iid+=1
    return sim_mat1,sim_mat2,pre_dict,suc_dict

def track_coms():
    ## Map communities
    # read jac data
    d1='2020-01-01'
    d2='2020-02-01'
    print(d1,d2)
    path="input path"
    jac=pd.read_csv(path,delimiter=' ',header=None) #_adjusted
    jac=jac.loc[(jac[2]>100)]
    jac_df=convert_jac_df(jac)
    
    map_com=dict()
    size_com=dict()
    
    map_com[d1]=dict()
    size_com[d1]=dict()
    I=len(jac_df)-1
    J=len(jac_df.columns)-1
    
    result_df=pd.DataFrame(index=[d1,d2],columns=[0])
    
    d1='2020-01-01'
    result_df.loc[d1,0]=list()
    ind=1
    end_ind=10000
    for i in range(I):
        if list(jac_df.index)[i]!=0:
            map_com[d1][list(jac_df.index)[i]]=ind
            size_com[d1][list(jac_df.index)[i]]=jac_df.iloc[i,-1]
            result_df.loc[d1,0].append(tuple(["",ind]))
            ind+=1
    
    d0=datetime(2020,1,1)
    d1=d0.date()
    
    for dd in range(1,30):
        if dd%12==0:
            d1=datetime(2020+(dd-1)//12,dd%12+12,1)
        else:
            d1=datetime(2020+dd//12,dd%12,1)
        
        if (dd+1)%12==0:
            d2=datetime(2020+(dd)//12,(dd+1)%12+12,1)
        else:
            d2=datetime(2020+(dd+1)//12,(dd+1)%12,1)
        print(d1,d2)
        
        d1=d1.date()
        d2=d2.date()
        d1=datetime.strftime(d1,"%Y-%m-%d")
        d2=datetime.strftime(d2,"%Y-%m-%d")
        #print(d1,end='\r')
        
        jac=pd.read_csv(path+d1+'_'+d2+'_adjusted.csv',delimiter=' ',header=None) #_adjusted
        jac=jac.loc[(jac[2]>100)]
        jac_df=convert_jac_df(jac)
        sim_mat1,sim_mat2,pre_dict,suc_dict=pre_suc_generator(jac_df)
        jac_df.iloc[:,:]=np.asarray(jac_df.iloc[:,:])/jac_df.iloc[-1,-1]
        
        map_com[d2]=dict()
        size_com[d2]=dict()
        result_df.loc[d2,0]=list()
        
        done_lst=list()
        done_lst2=list()
        for i in list(pre_dict.loc[:,'from']):
            #map_com
            j_lst=list()
            pair_lst=list()
            j_lst+=list(pre_dict.loc[pre_dict['from']==i,'to'])
            j_lst+=list(suc_dict.loc[suc_dict['from']==i,'to'])
            j_lst=list(set(list(j_lst)))
    
            for n in list(pre_dict.loc[pre_dict['from']==i].index):
                pair_lst.append(tuple(list(pre_dict.loc[n,['from','to','size']])))
            for n in list(suc_dict.loc[suc_dict['from']==i].index):
                pair_lst.append(tuple(list(suc_dict.loc[n,['from','to','size']])))
            
            for j in j_lst:
                #print(i,j,'-------')
                #print(suc_dict.loc[suc_dict['to']==j,['from','to','size']])
                for n in list(suc_dict.loc[suc_dict['to']==j].index):
                    pair_lst.append(tuple(list(suc_dict.loc[n,['from','to','size']])))
            pair_lst=list(set(list(pair_lst)))
            pair_lst=sorted(pair_lst, key=lambda x: x[2], reverse=True)

            # define scenarios like merge, split, growth, etc.
            sec=1
            for p in range(len(pair_lst)):
                if pair_lst[p] in done_lst2:
                    continue
                else:
                    done_lst2.append(pair_lst[p])
                
                size_com[d2][pair_lst[p][1]]=pair_lst[p][2]
                if pair_lst[p][0] not in map_com[d1].keys() and pair_lst[p][1] not in map_com[d2].keys():
                    #print('new',pair_lst[p][0])
                    map_com[d2][pair_lst[p][1]]=ind
                    result_df.loc[d2,0].append((0,ind,pair_lst[p][2]))
                    #print(pair_lst[p],result_df.iloc[-1,0][-1])
                    ind+=1
                    sec=1
                    continue
                
                if pair_lst[p][1]==0:
                    result_df.loc[d2,0].append((map_com[d1][pair_lst[p][0]],end_ind,pair_lst[p][2]))
                    end_ind=end_ind+1
                    sec=2
                    continue
                    
                if pair_lst[p][1] not in map_com[d2].keys():
                    if [pair[0] for pair in pair_lst[:p+1]].count(pair_lst[p][0])==1:
                        if map_com[d1][pair_lst[p][0]] not in map_com[d2].values():
                            map_com[d2][pair_lst[p][1]]=map_com[d1][pair_lst[p][0]]
                            result_df.loc[d2,0].append((map_com[d1][pair_lst[p][0]],map_com[d1][pair_lst[p][0]],pair_lst[p][2]))
                            sec=3
                        else:
                            split_seed=max([s for s in all_com if int(s)==int(map_com[d1][pair_lst[p][0]])])
                            map_com[d2][pair_lst[p][1]]=round(split_seed+0.01,2)
                            result_df.loc[d2,0].append((map_com[d1][pair_lst[p][0]],map_com[d2][pair_lst[p][1]],pair_lst[p][2]))
                            sec=3.1   
                    else:
                        all_com=list()
                        for k,v in map_com.items():
                            all_com+=v.values()
                        if len([s for s in all_com if int(s)==int(map_com[d1][pair_lst[p][0]])])>0:
                            split_seed=max([s for s in all_com if int(s)==int(map_com[d1][pair_lst[p][0]])])
                            sec=4
                        else:
                            #print('here')
                            #print(pair_lst[p][0],map_com[d1][pair_lst[p][0]],list(set(list(all_com))))
                            split_seed=map_com[d1][pair_lst[p][0]]
                            sec=5
                        map_com[d2][pair_lst[p][1]]=round(split_seed+0.01,2)
                        result_df.loc[d2,0].append((map_com[d1][pair_lst[p][0]],round(split_seed+0.01,2),pair_lst[p][2]))

                else:
                    if pair_lst[p][0] in map_com[d1].keys():
    
                        done_lst.append(pair_lst[p][0])
                        result_df.loc[d2,0].append((map_com[d1][pair_lst[p][0]],map_com[d2][pair_lst[p][1]],pair_lst[p][2]))
                        sec=6
    
                    else:
                        result_df.loc[d2,0].append((0,map_com[d2][pair_lst[p][1]],pair_lst[p][2]))
                        sec=7
  
                if dd==11:        
                    print(pair_lst[p],map_com[d2][pair_lst[p][1]],result_df.iloc[-1,0][-1])
                    print(sec)
                    #print(map_com[d2])
                    #print(result_df.loc[d2,0])
                    print('----------')
        result_df.loc[d2,0]=sorted(list(set(list(result_df.loc[d2,0]))), key=lambda x: x[0], reverse=False)

        if dd==11:
            print(result_df.loc[d2,0])

    return
        
    map_com2=dict()
    for ks,vs in map_com.items():
        map_com2[ks]=dict()
        for k,v in vs.items():
            map_com2[ks][v]=k
    return result_df


def main(result_df):
    I=30 # 30 months
    node_label=list()
    sankey_dict=dict()
    sankey_dict2=dict()
    color_index=1
    ind=0
    x=list()
    y=list()
    colors=['lightgrey','antiquewhite','crimson', 'cyan', 'aquamarine', 'azure', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
            'cornsilk',  'darkcyan','darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen','darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
            'aliceblue','darkblue', 'bisque', 'black','crimson','beige', 'cyan', 'blue','blueviolet', 'brown', 'antiquewhite', 'blanchedalmond']
    colors+=colors
    colors+=colors
    link_source=list()
    link_target=list()
    link_value=list()
    node_profile=pd.DataFrame(columns=['step','x','y','color','size','date','com_code'])
    
    for i in range(1,I):
        print(i,'--------------------')
        sankey_node_w=dict()
        d1=list(result_df.index)[i-1]
        d2=list(result_df.index)[i]
        sankey_dict[d2]=dict()
        sankey_dict2[d2]=dict()
        
            
        nodes_old_to=list(set(list(np.asarray(result_df.loc[d2,0])[:,1])))
        nodes_old_to
        nodes_size=dict()
        for n in nodes_old_to:
            nodes_size[n]=sum([t[2] for t in result_df.loc[d2,0] if t[1]==n])
        nodes_size=dict(sorted(nodes_size.items(), key=lambda item: item[1],reverse=True))
        thresh=0.01
        if i==1:
            key_nodes0=list()
            y_ind=0.1
    
            key_nodes_temp=[list(nodes_size.keys())[i] for i in range(len(nodes_size.values())) if list(nodes_size.values())[i]/sum(list(nodes_size.values()))>=0.01]
            sankey_dict[d1]=dict()
            sankey_dict[d2]=dict()
            sankey_dict2[d1]=dict()
            sankey_dict2[d2]=dict()
            
            #add initial nodes
            for t in result_df.loc[d2,0]:
                if t[1] in key_nodes_temp:
                    if t[0]!=0 and t[1]<10000 and t[0] not in key_nodes0 and t[2]>=np.sum(np.asarray(result_df.loc[d2,0])[:,2])*0.05: # only keep nodes that are larger than 5%
                        node_label.append(ind)
                        key_nodes0.append(t[0])
                        sankey_dict[d1][t[0]]=ind
                        sankey_dict2[d1][ind]=t[0]
                        node_profile.loc[ind,:]=[i-1,i,y_ind,color_index,t[2],d1,map_com2[d1][t[0]]]
                        ind+=1
                        y_ind=y_ind+0.05
                        color_index=color_index+1
            
        y_ind=0.1
        key_nodes_temp=[list(nodes_size.keys())[i] for i in range(len(nodes_size.values())) if list(nodes_size.values())[i]/sum(list(nodes_size.values()))>=thresh]
        key_nodes=list()
        for k in key_nodes0+key_nodes_temp:
            if k in key_nodes0 and k in key_nodes_temp:
                key_nodes.append(k)
            elif k not in key_nodes_temp and k<10000:
                #print(k,[[ii[0],ii[1],ii[2],np.round(ii[2]/sum(list(nodes_size.values())),2)] for ii in result_df.loc[d2,0] if ii[0]==k])
                if len([ii for ii in result_df.loc[d2,0] if ii[0]==k and ii[1]<10000 and ii[2]/sum(list(nodes_size.values()))>=0.01])>0:
                    key_nodes.append([ii[1] for ii in result_df.loc[d2,0] if ii[0]==k and ii[1]<10000][0])
            
        key_nodes=list(dict.fromkeys(key_nodes))
        print(key_nodes)
        for k in key_nodes:
            sankey_dict[d2][k]=ind
            sankey_dict2[d2][ind]=k
            node_label.append(ind)
            node_profile.loc[ind,:]=[i,i+1,y_ind,0,sum([ii[2] for ii in result_df.loc[d2,0] if ii[1]==k]),d2,map_com2[d2][k]]
            y_ind=y_ind+0.1
            ind+=1
        
        link_lst=list()
        for n in key_nodes0:
            link_lst+=[ii for ii in result_df.loc[d2,0] if ii[0]==n and ii[1] in key_nodes]
        
        
        link_source+=[sankey_dict[d1][ii[0]] for ii in link_lst]
        link_target+=[sankey_dict[d2][ii[1]] for ii in link_lst]
        link_value+=[ii[2] for ii in link_lst]
        
        # Adjust color of nodes
        done_lst=list()
        for l in link_lst:
            if sankey_dict[d2][l[1]] not in done_lst:
                node_profile.loc[sankey_dict[d2][l[1]],'color']=node_profile.loc[sankey_dict[d1][l[0]],'color']
                done_lst.append(sankey_dict[d2][l[1]])
                
                '''
                for tt in [link for link in link_lst if link[1]==l[1]]:
                    if node_profile.loc[sankey_dict[d1][tt[0]],'color']!=node_profile.loc[sankey_dict[d1][l[0]],'color'] and len([link for link in link_lst if link[0]==tt[0]])==1:
                        node_profile.loc[node_profile['color']==node_profile.loc[sankey_dict[d1][tt[0]],'color'],'color']=node_profile.loc[sankey_dict[d1][l[0]],'color']
                '''
                
        
        
        for k in key_nodes_temp:
            print(k)
            if k not in key_nodes0 and k not in key_nodes:
                temp=[ii for ii in result_df.loc[d2,0] if ii[0] in key_nodes0+[k] and ii[1]==k]
                
                if len(temp)>0:
                    for t in temp:
                        
                        if t[0] in key_nodes0:
                            #print('new but from existing node',t)
                            key_nodes.append(t[1])
                            sankey_dict[d2][t[1]]=ind
                            sankey_dict2[d2][ind]=t[1]
                            node_label.append(ind)
                            try:
                                node_profile.loc[ind,:]=[i,i+1,y_ind,color_index,sum([ii[2] for ii in result_df.loc[d2,0] if ii[1]==t[1]]),d2,map_com2[d2][t[1]]]
                            except:
                                node_profile.loc[ind,:]=[i,i+1,y_ind,color_index,sum([ii[2] for ii in result_df.loc[d2,0] if ii[1]==t[1]]),d2,0]
                            y_ind+=0.05
                            ind+=1
                            color_index+=1
    
                            link_source+=[sankey_dict[d1][t[0]]]
                            link_target+=[sankey_dict[d2][t[1]]]
                            link_value+=[t[2]]
                            break
                        else:
                            #print('new w/o existing node',t)
                            key_nodes0.append(t[0])
                            sankey_dict[d1][t[0]]=ind
                            sankey_dict2[d1][ind]=t[0]
                            node_label.append(ind)
                            node_profile.loc[ind,:]=[i-1,i,len(sankey_dict[d1].keys())*0.1+0.1,color_index,sum([ii[2] for ii in result_df.loc[d2,0] if ii[0]==t[0]]),d1,map_com2[d1][t[0]]]
                            ind+=1
    
                            key_nodes.append(t[1])
                            sankey_dict[d2][t[1]]=ind
                            sankey_dict2[d2][ind]=t[1]
                            node_label.append(ind)
                            try:
                                node_profile.loc[ind,:]=[i,i+1,y_ind,color_index,sum([ii[2] for ii in result_df.loc[d2,0] if ii[1]==t[1]]),d2,map_com2[d2][t[1]]]
                            except:
                                node_profile.loc[ind,:]=[i,i+1,y_ind,color_index,sum([ii[2] for ii in result_df.loc[d2,0] if ii[1]==t[1]]),d2,0]
                            y_ind+=0.05
                            ind+=1
                            color_index+=1
    
                            link_source+=[sankey_dict[d1][t[0]]]
                            link_target+=[sankey_dict[d2][t[1]]]
                            link_value+=[t[2]]
    
                            #print('new',k,'from:',t[0],', to:',t[1],', modifid_from:',sankey_dict[d1][t[0]],', modifid_to:',sankey_dict[d2][t[1]])
    
                            link_lst+=[t]
                            break
    
        key_nodes0=key_nodes
        print('--------------------------')
    
    #node_profile.loc[1,'y']=0.2
    #node_profile.loc[2,'y']=0.15
    #node_profile.loc[6,'y']=0.15
    #node_profile.loc[7,'y']=0.3
    
    
    x=list(np.asarray(node_profile.loc[:,'x'])/max(np.asarray(node_profile.loc[:,'x'])))
    y=list(node_profile.loc[:,'y'])
    fig = go.Figure(data=[go.Sankey(
        arrangement='snap',
        node = dict(thickness = 10,
          #label =  list(np.arange(0,nodes[-1]+1,1))
            label=node_label,
            color=[colors[cc] for cc in node_profile.loc[:,'color']],
            x=list(x),
            y=list(y)
            ),
            # Add links
    
            link = dict(
              source =  link_source,
              target =  link_target,
              value =  link_value,
              #label = link_label
        )
        )])
    fig.update_layout(font_size=8)
    fig.show()

if __name__ == "__main__":
    result_df=track_coms()
    main(result_df)
