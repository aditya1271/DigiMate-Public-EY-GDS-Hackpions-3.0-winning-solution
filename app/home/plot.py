import random
from jinja2 import Template
import pandas as pd
import numpy as np
import networkx as nx
from collections import Counter

def clevel(G,nodes,recommended,Graph):
  linkWith=[]
  done=[]
  a = set(recommended)
  for node in nodes:
    b=set(G.neighbors(node))
    common=a & b
    if(common):
      linkWith=list(common)  
    
    Graph.append({"name":node,"value":15,"linkWith":linkWith })
    
    linkWith=[]
    notlist=[]
    for x in common:
      children=[]
      if x not in done:
        ch=list(G.neighbors(x))
        #print("@@@@@@@@@@@",x,ch)
        i=0
        for y in ch:
          if y in common:
            linkWith.append(y)
          elif y in notlist:
            continue
          elif y !=node :
            i+=1
            notlist.append(y)
            children.append({"name":y,"value":5})
            if i>7:
              break
        Graph.append({"name":x,"value":10,"linkWith":linkWith,"children":children  })
        done.append(x)
    
def getRecommendations(ilist,flatJlist):

  G = nx.read_gpickle("graph.gpickle")
  alreadyRecommend=[]
  for r in ilist:
    if r!="None":
      alreadyRecommend.append(r)

  #alreadyRecommend.extend(skills)
  #print(alreadyRecommend)
  Graph=[]
  temp={}
  temp1={}
  #flatJlist = [j for sub in jlist for j in sub]
  counter = Counter(flatJlist)

  klist=counter.keys()
  for node in alreadyRecommend:
      l1=list(G.neighbors(node))
      for e in l1:
          if e in temp:
              temp[e]+=1
          else:
              temp[e]=1
          if e in klist:
            temp1[e]=counter[e]
          
      
  recommend=list(dict(sorted(temp.items(), key=lambda item: item[1],reverse=True)).keys())[:5]
  #TODO return
  crecommend=list(dict(sorted(temp1.items(), key=lambda item: item[1],reverse=True)).keys())[:5]

  l=recommend.copy()
  clevel(G,alreadyRecommend,recommend,Graph)
  #print(Graph)

  return crecommend,l,Graph
