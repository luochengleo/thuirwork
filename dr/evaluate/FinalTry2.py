#coding=utf8
from collections import defaultdict
fout = open('run.othermeasures.csv','w')
fout.write('runname,type,I-recall@20,D-nDCG@20\n')
run2irecall = defaultdict(lambda:0.0)
run2dndcg = defaultdict(lambda:0.0)
for l in open('cn.flseva.pertopic.csv').readlines()[1:]:
    segs = l.strip().split(',')
    runname  = segs[0]
    run2dndcg[runname]+= float(segs[2])
    run2irecall[runname]+= float(segs[4])
for r in run2irecall:
    fout.write(r+',coarse,'+str(run2dndcg[r]/32.0)+','+str(run2irecall[r]/32.0)+'\n')
    
    
run2irecall = defaultdict(lambda:0.0)
run2dndcg = defaultdict(lambda:0.0)

for l in open('cn.slseva.pertopic.csv').readlines()[1:]:
    segs = l.strip().split(',')
    runname  = segs[0]
    run2dndcg[runname]+= float(segs[2])
    run2irecall[runname]+= float(segs[4])
for r in run2irecall:
    fout.write(r+',fine,'+str(run2dndcg[r]/32.0)+','+str(run2irecall[r]/32.0)+'\n')

fout.write('\n\n\n')


run2irecall = defaultdict(lambda:0.0)
run2dndcg = defaultdict(lambda:0.0)
for l in open('en.flseva.pertopic.csv').readlines()[1:]:
    segs = l.strip().split(',')
    runname  = segs[0]
    run2dndcg[runname]+= float(segs[2])
    run2irecall[runname]+= float(segs[4])
for r in run2irecall:
    fout.write(r+',coarse,'+str(run2dndcg[r]/33.0)+','+str(run2irecall[r]/33.0)+'\n')
    
    
run2irecall = defaultdict(lambda:0.0)
run2dndcg = defaultdict(lambda:0.0)
for l in open('en.slseva.pertopic.csv').readlines()[1:]:
    segs = l.strip().split(',')
    runname  = segs[0]
    run2dndcg[runname]+= float(segs[2])
    run2irecall[runname]+= float(segs[4])
for r in run2irecall:
    fout.write(r+',fine,'+str(run2dndcg[r]/33.0)+','+str(run2irecall[r]/33.0)+'\n')
    
    