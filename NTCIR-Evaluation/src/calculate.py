#coding=utf8

#__author__=="LUO Cheng"
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
    [TopicID];0;[1st level Subtopic];[Rank1];[Score1];0;[2nd level Subtopic];[Rank2];[Score2];[RunName]\n
    rtr = list()
    for l in open(filename).readlines()[1:]:
        segs=  l.strip().split(';')
        topicid = segs[0]
        fls = segs[2]
        rankfls = segs[3]
        scorefls = segs[4]
        sls = segs[5]
        ranksls = segs[6]
        scoresls = segs[7]
        runname = segs[8]
        r = result(topicid, fls,rankfls,scorefls,sls,ranksls,scoresls,runname)
        rtr.append(r)
    return rtr
        

def calculteH(runname):
    filename = '../data/cnrun/'+runname+'.txt'
    results = loadfile(filename)
    accuracy = dict()
    for l in open('../data/csv/task2.csv'):
        queryid,fls,sls,accu = l.strip().split(',')
        accuracy[(queryid,fls,sls)] = int(accu)
    hscorelist = list()
        

