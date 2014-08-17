#coding=utf8

from collections import defaultdict
import os
import csv

def sort_by_value(d):
    items = d.items()
    backitems = [[v[1] , v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[i][1] for i in range(0,len(backitems))]

def loadcsv(filename):
    return csv.reader(open(filename))

def evaid():
    rtr = []
    for i in range(51,84,1):
        if i <10:
            rtr.append('000'+str(i))
        else:
            rtr.append('00'+str(i))
    return rtr

if 'flseva' not in os.listdir('../data'):
    os.mkdir('../data/flseva')

####################################################
userfls2annofls = defaultdict(lambda:'')
for l in loadcsv('../data/csv/task6.csv'):
    userfls2annofls[l[1]] = l[3]

####################################################
annofls2idx = dict()
id = ''
count = 1
iprob = open('../data/flseva/imine.Iprob','w')
for l in open('../data/temp/flsposs.txt').readlines():
    segs=  l.strip().split('\t')
    annofls = segs[1]
    id = segs[0]
    if segs[0] != id:
        count = 1
        id = segs[0]
    else:
        count +=1
    annofls2idx[(id,annofls)] = count
    iprob.write(id+' '+str(count)+' '+segs[2]+'\n')
for k in annofls2idx:
    print k,annofls2idx[k]
######################################################
run1 = open('../data/flseva/run1.sh','w')
runlist = open('../data/flseva/iminerunlist','w')
run2 = open('../data/flseva/run2.sh','w')
run2.write('cat ./iminerunlist | ./TRECsplitruns ./imine.Iprob.tid')
run2.close()

run3 = open('../data/flseva/run3.sh','w')


for f in os.listdir('../data/enrun'):
    run1.write('./DIN-splitqrels imine.Iprob '+f.replace('txt','Dqrels')+' imine'+'\n')
    runlist.write(f.replace('.txt','')+'\n')
    run3.write('echo '+f.replace('.txt','')+' | ./D-NTCIR-eval imine.Iprob.tid imine 5 100\n')
    print f
    dreq = open('../data/flseva/'+f.replace('txt','Dqrels'),'w')
    alreadyin = set()
    pairlist = list()
    for l in open('../data/enrun/'+f).readlines()[1:]:
        segs = l.strip().replace('&amp;','').split(';')
        id = segs[0]
        userfls = segs[2]
        flsrank = int(segs[3])
        if (id,userfls,flsrank) not in alreadyin:
            alreadyin.add((id,userfls,flsrank))
            pairlist.append((id,userfls,flsrank))
    
    for p in pairlist :
        id = p[0]
        if id in evaid():
            
            userfls = p[1]
            flsrank = p[2]
            annofls = userfls2annofls[userfls]
#             print id,userfls,flsrank,annofls

            if annofls !='':
                try:
                    intent = annofls2idx[(id,annofls)]
                except:
                    print '-------except-------'
                    print userfls
                    print annofls
                    bug = open('../data/out.debug','w')
                    bug.write('fail key '+annofls+'\n')
                    for item in annofls2idx.keys():
                        bug.write(item[0]+'\t'+item[1]+'\n')
                    bug.close()
                intent = 0
                if intent != 0:
                    rel = 'L1'
                else:
                    rel = 'L0'
            else:
                intent = 0
                rel = 'L0'
            dreq.write(id+' '+str(intent)+' '+userfls.replace(' ','')+' '+rel+'\n')
    dreq.close()

run1.close()
run3.close()
runlist.close()