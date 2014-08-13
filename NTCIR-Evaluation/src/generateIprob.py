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
    fout = open('../data/Dqrels/'+runname+'.Dqrels','w')
    for l in open('../data/cnrun/'+runname+'.txt').readlines()[1:]:
        segs = l.replace(codecs.BOM_UTF8,'').strip().split(';')
        id = segs[0]
        sls = segs[6]
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
            
        
        fout.write(id+' '+intent+' '+str(sls.__hash__())+' '+tag+'\n')
    fout.close()
import os
for f in os.listdir('../data/cnrun/'):
    print f
    generateDqrels(f.replace('.txt',''))
