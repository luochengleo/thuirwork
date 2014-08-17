#coding=utf8

from collections import defaultdict
import os
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
for l in loadcsv('../data/csv/task3.csv'):
    userfls2annofls[l[1]] = l[3]

####################################################
annofls2idx = dict()
id = ''
count = 1
iprob = open('../data/flseva/imine.Iprob','w')
for l in open('../data/temp/flsposs.txt').readlines():
    segs=  l.strip().split('\t')
    annofls = segs[1]
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

allsubfls = defaultdict(lambda:set())
dqrels = open('../data/flseva/imine.Dqrels','w')
for f in os.listdir('../data/enrun'):
    print f

    for l in open('../data/enrun/'+f).readlines()[1:]:
        segs = l.strip().replace('&amp;','').split(';')
        id = segs[0]
        userfls = segs[2]
        flsrank = int(segs[3])
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

for f in os.listdir('../data/enrun'):
    runlist.write(f.replace('txt','run')+'\n')
    runout = open('../data/flseva/'+f.replace('txt','run'),'w')
    alreadyin = set()
    allsubfls = defaultdict(lambda:list())

    for l in open('../data/enrun/'+f).readlines()[1:]:
        segs = l.strip().replace('&amp;','').split(';')
        id = segs[0]
        userfls = segs[2]
        userflsrank = segs[3]
        userflsscore = segs[4]
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