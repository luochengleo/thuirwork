#coding=utf8

#__author__=="LUO Cheng"
import os
import codecs

import math
from collections import defaultdict
class result:
    def __init__(self,topicid, fls,rankfls,scorefls,sls,ranksls,scoresls,runname):
        self.topicid = topicid
        self.fls = fls
        self.rankfls = rankfls
        self.scorefls = scorefls
        self.sls = sls
        self.ranksls = ranksls
        self.scoresls = scoresls
        self.runname = runname
def loadfile(filename):
#[TopicID];0;[1st level Subtopic];[Rank1];[Score1];0;[2nd level Subtopic];[Rank2];[Score2];[RunName]\n
    rtr = list()
    for l in open(filename).readlines()[1:]:
        segs=  l.replace(codecs.BOM_UTF8,'').replace(codecs.BOM_UTF8,'').strip().split(';')
        topicid = segs[0]
        fls = segs[2]
        rankfls = segs[3]
        scorefls = segs[4]
        sls = segs[6]
        ranksls = segs[7]
        scoresls = segs[8]
        runname = segs[9]
        r = result(topicid, fls,rankfls,scorefls,sls,ranksls,scoresls,runname)
        rtr.append(r)
    return rtr
        

def calculateHscore(runname):
    
    filename = '../data/cnrun/'+runname+'.txt'
    results = loadfile(filename)
    accuracy = dict()
    
    hcount = defaultdict(lambda:defaultdict(lambda:0))
    hscore = defaultdict(lambda:defaultdict(lambda:0))
    
    
    for l in open('../data/csv/task2.csv'):
        queryid,fls,sls,accu = l.strip().split(',')
        if queryid.isdigit():
            accuracy[(queryid,fls,sls)] = int(accu)
    
    for item in results:
        topicid = item.topicid
        rankfls = item.rankfls
        
        if int(topicid)<34:
            try:
                accu = accuracy[(item.topicid,item.fls,item.sls)]

            except:
                accu = 0
            hscore[topicid][rankfls]+=(accu)
            hcount[topicid][rankfls]+=1
#         if (item.topicid,item.fls,item.sls) in accuracy:
#             print item.topicid,item.rankfls,item.ranksls,'hit',accuracy[(item.topicid,item.fls,item.sls)]
#         else:
#             print item.topicid,item.rankfls,item.ranksls,'miss','0'
        
    h_score_fls = defaultdict(lambda:defaultdict(lambda:0))
    for t in hscore:
        for f in hscore[t]:
            h_score_fls[t][f] = float(hscore[t][f])/float(hcount[t][f])
    
    rtr = list()
    for t in evaid():
        sum = 0.0
        for f in h_score_fls[t]:
            sum +=h_score_fls[t][f]
        try:
            rtr.append(sum/float(len(h_score_fls[t].keys())))
        except:
            rtr.append(0.0)
    return rtr
        
        
    
    
def dcg( r ):
    rtr = list()
    for i in range(0,len(r),1):
        if i == 0:
            rtr.append(float(r[0]))
        else:
            rtr.append(rtr[-1]+r[i]/math.log(i+1,2))
    return rtr
def ndcg(r ):
    if len(r)==0:
        return [0.0]
    dcg_ = dcg(r)
    idcg_ = dcg(sorted(r,reverse = True))
    if idcg_[0] <=0.0:
        return [0.0] * len(r)
    else:
        return [dcg_[i]/idcg_[i] for i in range(0,len(r),1)]
# def ndcg( r ): 
#     from operator import div
#     return map(div, dcg(r), dcg(sorted(r, reverse=True)))
def evaid():
    rtr = []
    for i in range(1,34,1):
        if i <10:
            rtr.append('000'+str(i))
        else:
            rtr.append('00'+str(i))
    return rtr
def mean(r):
    rtr = 0.0
    for item in r:
        rtr+= float(item)
    if rtr == 0 :
        return 0.0
    else:
        return rtr/float(len(r))
def calculateFscore(runname):
    
    filename = '../data/cnrun/'+runname+'.txt'
    results = loadfile(filename)
    flsrel = dict()
    queryid = set()
    for l in open('../data/csv/task1.csv'):
        segs = l.replace(codecs.BOM_UTF8,'').strip().split(',')
        id = segs[0]
        fls = segs[1]
        rel = int(segs[3])
        flsrel[(id,fls)] = rel
        queryid.add(id)

    fls = defaultdict(lambda : list())
    alreadyin = defaultdict(lambda: set())
    for r in results:
        if r.topicid in queryid and r.fls not in alreadyin[r.topicid]:
            try:
                fls[r.topicid].append(flsrel[(r.topicid,r.fls)])
            except:
                print 'miss',r.topicid,r.fls
                fls[r.topicid].append(0)
            alreadyin[r.topicid].add(r.fls)
    rtr = []
    for id in evaid():
        rtr.append(ndcg(fls[id])[-1])
    return rtr


if __name__=="__main__":
#     print calculateHscore('CNU-S-C-2A')
#     print len(calculateHscore('CNU-S-C-2A'))
#     print calculateHscore('CNU-S-C-2A')
    for f in os.listdir('../data/cnrun/'):
        runname = f.replace('.txt','')
        print runname,'\t',mean(calculateFscore(runname))
