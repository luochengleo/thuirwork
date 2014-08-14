#coding=utf8
import codecs
from collections import defaultdict



def sort_by_value(d):
    items = d.items()
    backitems = [[v[1] , v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[i][1] for i in range(0,len(backitems))]

def evaid():
    rtr = []
    for i in range(1,34,1):
        if i <10:
            rtr.append('000'+str(i))
        else:
            rtr.append('00'+str(i))
    return rtr


flsposs = defaultdict(lambda:dict())

idandfls2idx = defaultdict(lambda:dict())

for l in open('../data/temp/flsposs.txt'):
    segs = l.strip().replace(codecs.BOM_UTF8,'').split('\t')
    queryid = segs[0]
    fls = segs[1]
    poss = float(segs[2])
    flsposs[queryid][fls] = poss

debugout = open('../data/temp/iprob.debug.txt','w')
fout = open('../data/Dqrels/imine.Iprob','w')
for id in evaid():
    sorted_fls = sort_by_value(flsposs[id])
    for i in range(1,len(sorted_fls)+1,1):
        idandfls2idx[id][sorted_fls[i-1]] = i
        print 'add ', id , sorted_fls[i-1],i,('unicode',sorted_fls[i-1])
        fout.write(id+' '+str(i)+' '+str(flsposs[id][sorted_fls[i-1]])+'\n')
        debugout.write(id+' '+str(i)+' '+str(flsposs[id][sorted_fls[i-1]])+'\t'+sorted_fls[i-1]+'\n')

fout.close()

idandsls2fls = dict()
for l in open('../data/csv/task6.csv'):
    segs = l.replace(codecs.BOM_UTF8,'').split(',')
    id = segs[0]
    if len(id) ==1:
        id = '000'+id
    else:
        id = '00'+id
    query = segs[1]
    fls = segs[3]
    idandsls2fls[(id,query)] = fls

def generateDqrels(runname):
    fout = open('../data/Dqrels/sakai/'+runname+'.Dqrels','w')
    trec = open('../data/Dqrels/sakai/'+runname +'.run','w')
    for l in open('../data/cnrun/'+runname+'.txt').readlines()[1:]:
        segs = l.replace(codecs.BOM_UTF8,'').strip().split(';')
        id = segs[0]
        sls = segs[6]
        slsrank = segs[7]
        slsscore = segs[8]
        try:
            fls = idandsls2fls[(id,sls)]
        except:
            fls = ''
        
        if fls =='':
            intent = '0'
            tag = "L0"
        else:
            try:
                intent = str(idandfls2idx[id][fls])
                tag = "L1"
            except:
                intent = '0'
                tag = 'L0'
                print 'except',id,fls
            
        docid = str(sls.__hash__()).replace('-','')
        fout.write(id+' '+intent+' '+docid+' '+tag+'\n')
        trec.write(id+' Q0 '+docid+' '+slsrank+' '+slsscore+' '+runname+'\n')
    trec.close()
    fout.close()
import os
runlist = open('../data/Dqrels/sakai/ownrunlist','w')
batch = open('../data/Dqrels/sakai/batch.sh','w')
evaluate = open('../data/Dqrels/sakai/evaluate.sh','w')
for f in os.listdir('../data/cnrun/'):
    print f
    generateDqrels(f.replace('.txt',''))
    runname =f.replace('.txt','')
    runlist.write(f.replace('.txt','.run')+'\n')
    batch.write('./DIN-splitqrels imine.Iprob '+f.replace('.txt','')+'.Dqrels'+' '+f.replace('.txt','')+'\n')
    evaluate.write('echo '+runname+'.run | ./D-NTCIR-eval imine.Iprob.tid '+runname+' 10 110\n')
runlist.close()
batch.close()
