#coding=utf8
#__author__=='luocheng'

TAG = 'cn'
start = 1
end =51
switch = 33
devide = 49.0
from collections import defaultdict

run2id2fls_ndcg = defaultdict(lambda:defaultdict(lambda:0))
run2id2sls_ndcg = defaultdict(lambda:defaultdict(lambda:0))
run2id2ndcg = defaultdict(lambda:defaultdict(lambda:0))

for l in open('./'+TAG+'.flseva.pertopic.csv').readlines()[1:]:
    segs=  l.strip().split(',')
    runname = segs[0]
    id = segs[1]
    dsharp = float(segs[3])
    run2id2fls_ndcg[runname][id] = dsharp

for l in open('./'+TAG+'.slseva.pertopic.csv').readlines()[1:]:
    segs=  l.strip().split(',')
    runname = segs[0]
    id = segs[1]
    dsharp = float(segs[3])
    run2id2sls_ndcg[runname][id] = dsharp

for l in open('./'+TAG+'.ndcg.pertopic.csv').readlines():
    segs=  l.strip().split(',')
    runname = segs[0]
    id = segs[1]
    ndcg= float(segs[2])
    run2id2ndcg[runname][id] = ndcg

def evaid():
    rtr = list()
    for i in range(start,end,1):
        if i <10:
            rtr.append('000'+str(i))
        if i >10 and i <100:
            rtr.append('00'+str(i))
        if i >=100:
            rtr.append('0'+str(i))
    return rtr
run2coarsesum =defaultdict(lambda:0.0)
run2finesum =defaultdict(lambda:0.0)

fout = open(TAG+'.dr.pertopic.csv','w')
fout.write('runname,id,coarse,fine,ndcg\n')
for r in sorted(list(run2id2ndcg.keys())):
    for id in evaid():
        if int(id) < switch:
            run2coarsesum[r] += run2id2fls_ndcg[r][id]
            run2finesum[r] += run2id2sls_ndcg[r][id]
        else:
            run2coarsesum[r] += run2id2ndcg[r][id]
            run2finesum[r] += run2id2ndcg[r][id]

        fout.write(r+','+id+','+str(run2id2fls_ndcg[r][id])+','+str(run2id2sls_ndcg[r][id])+','+str(run2id2ndcg[r][id])+'\n')    
fout.close()

fout = open(TAG+'.dr.perrun.csv','w')
fout.write('runname,coarse-score,fine-score\n')
for r in sorted(list(run2id2fls_ndcg.keys())):
    fout.write(r+','+str(run2coarsesum[r]/devide)+','+str(run2finesum[r]/devide)+'\n')
fout.close()

