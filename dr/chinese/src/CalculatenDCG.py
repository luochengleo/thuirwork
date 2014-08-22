#coding=utf8
from collections import defaultdict
import math,os

id2doc2rel=defaultdict(lambda: defaultdict(lambda:0))
id2idealDCG = dict()
cutoff = 20
start = 1
end = 51
query2id = dict()

def evaid():
    rtr = []
    for i in range(start,end,1):
        if len(str(i)) == 1:
            rtr.append('000'+str(i))
        if len(str(i)) == 2:
            rtr.append('00'+str(i))
        if len(str(i)) == 3:
            rtr.append('0'+str(i))
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

for l in open('../data/temp/IMine.Query.txt'):
    id,query = l.strip().split('\t')
    query2id[query] =  id

for l in open('../data/csv/dr1.csv'):
    segs = l.strip().split(',')
    queryid = segs[0]
    if len(queryid) ==1:
        queryid = '000'+queryid
    if len(queryid) ==2:
        queryid = '00'+queryid
    docid = segs[1]
    rel = int(segs[2])
    id2doc2rel[queryid][docid] = rel

for id in id2doc2rel:
    rellist = list()
    for doc in id2doc2rel[id]:
        rellist.append(id2doc2rel[id][doc])
    id2idealDCG[id] = dcg(sorted(rellist,reverse=True))

fout = open('../data/ndcg.pertopic.csv','w')

for run in os.listdir('../data/run'):
    if run != '.DS_Store':
        runname = run.replace('.txt','')
        print runname
        id2rellist = defaultdict(lambda:list())
        id2dcg = dict()
        
        for l in open('../data/run/'+run).readlines()[1:]:
            segs  = l.strip().split(' ')
            id =segs[0]
            doc = segs[2]
            rel = id2doc2rel[id][doc]
            id2rellist[id].append(rel)
        for id in id2rellist:
            print run,'id',id
            id2dcg[id] = dcg(id2rellist[id])
        for id in evaid():
            if id in id2dcg:
                if len(id2dcg[id])>cutoff:
                    ndcg_ = float(id2dcg[id][cutoff-1])/float(id2idealDCG[id][cutoff-1])
                else:
                    print 'too less results'
                fout.write(runname+','+id+","+str(ndcg_)+'\n')
            else:
                fout.write(runname+','+id+","+str(0.0)+'\n')
fout.close()
        