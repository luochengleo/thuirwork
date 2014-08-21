#coding=utf8

from collections import defaultdict
import os
import codecs

import csv
def str2id(s):
    return str(s.__hash__()).replace('-','')
def sort_by_value(d):
    items = d.items()
    backitems = [[v[1] , v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[i][1] for i in range(0,len(backitems))]

def loadcsv(filename):
    return csv.reader(open(filename))

def evaid():
    rtr = []
    for i in range(1,34,1):
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
    userfls2annofls[l[1].strip()] = l[3].strip()
for l in loadcsv('../data/csv/task3.csv'):
    if l[1].strip() not in userfls2annofls.keys():
        print 'suplement',l[1].strip(),l[2].strip()
        userfls2annofls[l[1].strip()] = l[2].strip()
####################################################
annofls2idx = dict()
id = ''
count = 1
iprob = open('../data/flseva/imine.Iprob','w')
for l in open('../data/temp/flsposs.txt').readlines():
    segs=  l.strip().split('\t')
    annofls = segs[1].strip()
    if segs[0] != id:
        count = 1
        id = segs[0].strip()
    else:
        count +=1
    annofls2idx[(id,annofls)] = count
    iprob.write(id+' '+str(count)+' '+segs[2]+'\n')
for k in annofls2idx:
    print k,annofls2idx[k]
######################################################

allsubfls = defaultdict(lambda:set())
dqrels = open('../data/flseva/imine.Dqrels','w')
for f in os.listdir('../data/cnrun'):
    print f
    for l in open('../data/cnrun/'+f).readlines()[1:]:
        segs = l.strip().replace('&amp;','').split(';')
        id = segs[0].strip()
        userfls = segs[2].strip()
        flsrank = int(segs[3].strip())
        allsubfls[id].add(userfls)
    
    for id in evaid():
        for ufls in allsubfls[id]:
            annofls = userfls2annofls[ufls]
            if annofls != '':
                try:
                    intent = annofls2idx[(id,annofls)]
                except:
                    print '-------except-------'
                    print id
                    print ufls
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
            dqrels.write(id+' '+str(intent)+' '+str2id(ufls)+' '+rel+'\n')


#############################################################################
runlist = open('../data/flseva/iminerunlist','w')

for f in os.listdir('../data/cnrun'):
    runlist.write(f.replace('txt','run')+'\n')
    runout = open('../data/flseva/'+f.replace('txt','run'),'w')
    alreadyin = set()
    allsubfls = defaultdict(lambda:list())

    for l in open('../data/cnrun/'+f).readlines()[1:]:
        segs = l.strip().replace('&amp;','').split(';')
        id = segs[0].strip()
        userfls = segs[2].strip()
        userflsrank = segs[3].strip()
        userflsscore = segs[4].strip()
        if (userfls,userflsrank,userflsscore) in alreadyin:
            continue
        else:
            alreadyin.add((userfls,userflsrank,userflsscore))
            allsubfls[id].append((userfls,userflsrank,userflsscore))
        
    for id in evaid():
        for sub in allsubfls[id]:
            runout.write(id+' Q0 '+str2id(sub[0])+' '+sub[1]+' '+sub[2]+' '+f.replace('.txt','')+'\n')
    runout.close()
runlist.close()