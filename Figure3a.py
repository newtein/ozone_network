
# coding: utf-8

# In[1]:


import pickle
import matplotlib.pyplot as plt
import pickle
import networkx as nx
import  functools
import math
import numpy as np
import os
from decimal import Decimal
from collections import OrderedDict
import subprocess as sp


# In[2]:


import operator as op
def nCr(n,r):
    f = math.factorial
    return Decimal(f(n)) / (Decimal(f(r)) * Decimal(f(n-r)))

def calculatep(N,k,pi):
    return nCr(N-1,k)*Decimal(pow(pi,k))*Decimal(pow(1-pi,N-1-k))


def setplot(plt):
   
    ax = plt.subplot(111) 

    ax.spines["top"].set_visible(False)  
    ax.spines["bottom"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(False)

    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()  
    return plt,ax

def excecuteCommand(command):
    command=command.split()
    process = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = process.communicate()
    print(stdout,stderr,"ok")
    return


# In[3]:


target="Com"
G=pickle.load(open('{}/Graph.pickle'.format(target),"rb"))
waveMatrix=pickle.load(open('{}/waveMatrix.pickle'.format(target),"rb"))
skip=pickle.load(open('{}/skip.pickle'.format(target),"rb"))
nodeNames=pickle.load(open('{}/Correlations/o3/2017/nodeNames.pickle'.format(target),"rb"))


# In[4]:


networkDetails=open('{}/CorrelationSummary/networkfeautures.csv'.format(target),'r').readline().strip().split(',')

try:
    cluster=pickle.load(open('{}/cluster.pickle'.format(target),'rb'))
    degree=pickle.load(open('{}/degree.pickle'.format(target),'rb'))
except:
    cluster=nx.clustering(G,weight='weight')
    degree=nx.degree(G,weight='weight')
    pickle.dump(cluster,open('{}/cluster.pickle'.format(target),'wb'))
    pickle.dump(degree,open('{}/degree.pickle'.format(target),'wb'))
    
kmean=float(networkDetails[3])
pi=float(networkDetails[-2])
N=len(degree)
Cavg=float(networkDetails[-1])


# In[5]:


from networkx.algorithms import community

def bisectGraph(G,name1,name2):
    c=community.kernighan_lin_bisection(G,weight='weight')
    pickle.dump(list(c[0]),open("community/a/{}.pickle".format(name1),"wb"))
    pickle.dump(list(c[1]),open("community/a/{}.pickle".format(name2),"wb"))
    print('py -3 plotBasemap.py {}'.format(name1))
    excecuteCommand('py -3 plotBasemap.py {} a'.format(name1))
    excecuteCommand('py -3 plotBasemap.py {} a'.format(name2))
    #print(a,b)
    print('Done!')
    return G.subgraph(c[0]),G.subgraph(c[1]),c

def greedyModularity(G,name1):
    c = list(community.asyn_lpa_communities(G,weight='weight'))
    print(len(c))
   
    for i in range(len(c)):
        pickle.dump(list(c[i]),open("community/b/{}{}.pickle".format(name1,i),"wb"))   
        excecuteCommand('py -3 plotBasemap.py {}{} {}'.format(name1,i,'b'))
        graphList.append(G.subgraph(c[i]))
    print('Done!')
    return graphList,c

def pythonLouveinCom(G,name1):
    partition=pylc.best_partition(G,weight='weight')
    graphList,nodeList=[],[]
    count=0
    print('ok','c')
    for com in set(partition.values()) :
        count = count + 1
        list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
        pickle.dump(list_nodes,open("community/c/{}{}.pickle".format(name1,count),"wb"))   
        excecuteCommand('py -3 plotBasemap.py {}{} {}'.format(name1,count,'c'))
        graphList.append(G.subgraph(list_nodes))
        nodeList.append(set(list_nodes))
       
    return graphList,nodeList


# In[13]:


# k - lin

G1,G2,c=bisectGraph(G,1,2)
community.modularity(G,c,weight='weight')
print(1,2,community.modularity(G,c,weight='weight'))
print(G1.number_of_nodes(),G2.number_of_nodes())


# In[14]:


G11,G12,c1=bisectGraph(G1,11,12)


print(11,12,community.modularity(G,[c1[0],c1[1],c[1]],weight='weight'))
print(G11.number_of_nodes(),G12.number_of_nodes())


# In[15]:


G21,G22,c2=bisectGraph(G2,21,22)


print(21,22,community.modularity(G,[c[0],c2[0],c2[1]],weight='weight'))
print(G21.number_of_nodes(),G22.number_of_nodes())


# In[151]:


G111,G112,c11=bisectGraph(G11,111,112)
G121,G122,c12=bisectGraph(G12,121,122)


# In[113]:


G211,G212,c21=bisectGraph(G21,211,212)

print(211,212,community.modularity(G,[c[0],c21[0],c21[1],c2[1]],weight='weight'))
print(G211.number_of_nodes(),G212.number_of_nodes())

# In[114]:


G221,G222,c22=bisectGraph(G22,221,222)

print(221,222,community.modularity(G,[c[0],c2[0],c22[0],c22[1]],weight='weight'))
print(G221.number_of_nodes(),G222.number_of_nodes())


# In[71]:


GList,c=greedyModularity(G,1)
community.modularity(G,c,weight='weight')


# In[103]:


GList,NList=pythonLouveinCom(G,1)


# In[94]:


community.modularity(G,NList,weight='weight')


# In[95]:


GList1,NList1=pythonLouveinCom(GList[0],11)


# In[96]:


community.modularity(G,[NList1[0],NList1[1],NList1[2],NList[1],NList[2]],weight='weight')


# In[97]:


GList2,NList2=pythonLouveinCom(GList[1],22)


# In[98]:


community.modularity(G,[NList[0],NList2[0],NList2[1],NList[2]],weight='weight')


# In[99]:


GList3,NList3=pythonLouveinCom(GList[2],33)


# In[100]:


community.modularity(G,[NList[0],NList[1],NList3[0],NList3[1],NList3[2]],weight='weight')


# In[159]:


carbA=[6,41,53,35]
carbB=[9,10,23,24,25,34,36,42,44,50,11]
# c[0],c2[0],c2[1]


# In[140]:


stateCodes=pickle.load(open("stateCode.pickle","rb"))
degreeDict={}
for i in degree:
    degreeDict[i[0]]=i[1]


# In[161]:


a,b,o=0,0,0
total=0
cA,cB,otherState=set(),set(),set()
for temp in c12[0]:
    key=int(temp.split('-')[0])
    if key in carbA:
        #a+=degreeDict[temp]
        a+=1
        cA.add(key)
    elif key in carbB:
        #b+=degreeDict[temp]
        b+=1
        cB.add(key)
    else:
        #print()
        otherState.add(key)
        #o+=degreeDict[temp]
        o+=1
    total+=1

print(a*100/total,b*100/total,o*100/total)
print([stateCodes[int(i)] for i in cA]) 
print([stateCodes[int(i)] for i in cB]) 
print([stateCodes[int(i)] for i in otherState])  


# In[133]:


degreeDict[temp]

