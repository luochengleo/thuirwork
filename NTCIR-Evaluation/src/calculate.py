#coding=utf8

#__author__=="LUO Cheng"
import os
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
        segs=  l.strip().split(';')
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
        

def calculateH(runname):
    filename = '../data/cnrun/'+runname+'.txt'
    results = loadfile(filename)
    accuracy = dict()
    hscorelist = list()
    accudict  = defaultdict(lambda:list())
    
    for l in open('../data/csv/task2.csv'):
        print len(l.split(','))
        queryid,fls,sls,accu = l.strip().split(',')
        if queryid.isdigit():
            accuracy[(queryid,fls,sls)] = int(accu)
    for item in results:
        topicid = item.topicid
        if int(topicid)<34:
            try:
                accudict[topicid].append(accuracy[(item.topicid,item.fls,item.sls)])
            except:
                print 'EXCEPT',item.topicid,item.fls,item.sls
                
    
    for item in accudict:
        print item ,accudict[item]

if __name__=="__main__":
    calculateH("THUSAM-S-C-1A")
    all = set()
    for f in os.listdir('../data/cnrun/'):
        runname = f.replace('.txt','')
        for item in loadfile('../data/cnrun/'+f):
            if int(item.topicid)<34:
                all.add((item.topicid,item.fls,item.sls))
    print len(all)
    
