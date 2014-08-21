#coding=utf8

#__author__=="LUO Cheng"
import os
import codecs
import csv
def loadcsv(filename):
    return csv.reader(open(filename))
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
    
    filename = '../data/jprun/'+runname+'.txt'
    results = loadfile(filename)
    accuracy = dict()
    
    hcount = defaultdict(lambda:defaultdict(lambda:0))
    hscore = defaultdict(lambda:defaultdict(lambda:0))
    
    
    for l in loadcsv('../data/csv/task2.csv'):
        queryid = l[0]
        fls = l[1]
        sls = l[2]
        accu = l[3] 
        if queryid.isdigit():
            accuracy[('0'+queryid,fls,sls)] = int(accu)
    
    for item in results:
        topicid = item.topicid
        rankfls = item.rankfls
        
        if int(topicid)<135:
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

def evaid():
    rtr = []
    for i in range(101,135,1):
        rtr.append('0'+str(i))
    return rtr
def mean(r):
    rtr = 0.0
    for item in r:
        rtr+= float(item)
    if rtr == 0 :
        return 0.0
    else:
        return rtr/float(len(r))


if __name__=="__main__":
#     print calculateHscore('CNU-S-C-2A')
#     print len(calculateHscore('CNU-S-C-2A'))
#     print calculateHscore('CNU-S-C-2A')
    fout = open('../data/jphscorepertopic.csv','w')
    for f in os.listdir('../data/jprun/'):
        runname = f.replace('.txt','')
        print runname,mean(calculateHscore(runname))
        count =101
        for item in calculateHscore(runname):
            fout.write(runname+','+str(count)+','+str(item)+'\n')
            count +=1
    fout.close()
