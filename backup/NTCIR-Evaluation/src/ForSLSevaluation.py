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
    for i in range(1,34,1):
        if i <10:
            rtr.append('000'+str(i))
        else:
            rtr.append('00'+str(i))
    return rtr

if 'slseva' not in os.listdir('../data'):
    os.mkdir('../data/slseva')

####################################################
usersls2annosls = defaultdict(lambda:'')
for l in loadcsv('../data/csv/task6.csv'):
    usersls2annosls[l[1].strip()] = l[4].strip()

####################################################
annosls2idx = dict()
id = ''
count = 1
iprob = open('../data/slseva/imine.Iprob','w')
for l in open('../data/temp/slsposs.txt').readlines():
    segs=  l.strip().split('\t')
    annosls = segs[1].strip()
    if segs[0] != id:
        count = 1
        id = segs[0].strip()
    else:
        count +=1
    annosls2idx[(id,annosls)] = count
    iprob.write(id+' '+str(count)+' '+segs[2]+'\n')
for k in annosls2idx:
    print k,annosls2idx[k]
######################################################

allsubsls = defaultdict(lambda:set())
dqrels = open('../data/slseva/imine.Dqrels','w')
for f in os.listdir('../data/cnrun'):
    print f
    for l in open('../data/cnrun/'+f).readlines()[1:]:
        segs = l.strip().replace('&amp;','').split(';')
        id = segs[0].strip()
        usersls = segs[6].strip()
        slsrank = int(segs[3].strip())
        allsubsls[id].add(usersls)
    
for id in evaid():
    for usls in allsubsls[id]:
        annosls = usersls2annosls[usls]
        if annosls != '':
            try:
                intent = annosls2idx[(id,annosls)]
            except:
                print '-------except-------'
                print id
                print usls
                print annosls
                bug = open('../data/out.sls.debug','w')
                bug.write('fail key '+annosls+'\n')
                for item in annosls2idx.keys():
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
        dqrels.write(id+' '+str(intent)+' '+str2id(usls)+' '+rel+'\n')


#############################################################################
runlist = open('../data/slseva/iminerunlist','w')

for f in os.listdir('../data/cnrun'):
    runlist.write(f.replace('txt','run')+'\n')
    runout = open('../data/slseva/'+f.replace('txt','run'),'w')
    alreadyin = set()
    allsubsls = defaultdict(lambda:list())

    for l in open('../data/cnrun/'+f).readlines()[1:]:
        segs = l.strip().replace('&amp;','').split(';')
        id = segs[0].strip()
        usersls = segs[6].strip()
        userslsrank = segs[7].strip()
        userslsscore = segs[8].strip()
        if (usersls,userslsrank,userslsscore) in alreadyin:
            continue
        else:
            alreadyin.add((usersls,userslsrank,userslsscore))
            allsubsls[id].append((usersls,userslsrank,userslsscore))
        
    for id in evaid():
        for sub in allsubsls[id]:
            runout.write(id+' Q0 '+str2id(sub[0])+' '+sub[1]+' '+sub[2]+' '+f.replace('.txt','')+'\n')
    runout.close()
runlist.close()