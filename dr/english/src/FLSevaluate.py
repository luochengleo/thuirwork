#coding=utf8

from collections import defaultdict
import os
import codecs
import csv


start = 51
end = 84
query2id = dict()
for l in open('../data/temp/IMine.Query.txt'):
    id,query = l.strip().split('\t')
    query2id[query] =  id

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
    for i in range(start,end,1):
        if len(str(i)) == 1:
            rtr.append('000'+str(i))
        if len(str(i)) == 2:
            rtr.append('00'+str(i))
        if len(str(i)) == 3:
            rtr.append('0'+str(i))
    return rtr
def sls2fls(sls):
    segs = sls.strip().split('_')
    if len(segs)==2:
        return segs[0]
    if len(segs)==3:
        return segs[0]+'_'+segs[1]


if 'flseva' not in os.listdir('../data'):
    os.mkdir('../data/flseva')


###################################################
docid2annofls = defaultdict(lambda:set())
docid2rel = defaultdict(lambda: 0)
for l in loadcsv('../data/csv/dr2.csv'):
    query = l[0]
    queryid = query2id[l[0]]
    if len(queryid ) ==2:
        queryid='00'+queryid
    if len(queryid ) ==3:
        queryid ='0'+queryid
    if len(queryid) ==1:
        queryid = '000'+queryid
    docid= l[1].strip()
    rel = l[2].strip()
    slses = l[3:]
    print l[0],queryid
    for item in slses:
        if item !='':
            docid2rel[(queryid,docid)] = int(rel)
            docid2annofls[(queryid,docid)].add(sls2fls(item))
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

######################################################
# 0101 0 clueweb12-0006-97-23810 1 27.73 MSRA-D-E-1A

debug = open('../data/debug.txt','w')
allsubdocs = defaultdict(lambda:set())
dqrels = open('../data/flseva/imine.Dqrels','w')
for f in os.listdir('../data/run'):
    print f
    for l in open('../data/run/'+f).readlines()[1:]:
        segs = l.strip().replace('&amp;','').split(' ')
        id = segs[0].strip()
        docid  = segs[2].strip()
        allsubdocs[id].add(docid)
        debug.write(f+' '+id+' '+docid+'\n')
debug.close()
    
for id in evaid():
    for doc in allsubdocs[id]:
        annofls = docid2annofls[(id,doc)]
#         print id,doc,annofls
        if len(annofls) ==0:
            dqrels.write(id+' 0 '+doc+' L0\n')
        else:
            for fls_ in annofls:
                try:
                    intent = annofls2idx[(id,fls_)]
                except:
                    print '-------except-------'
                    print id
                    print doc
                    print fls_
                    bug = open('../data/out.debug','w')
                    bug.write('fail key '+fls_+'\n')
                    for item in annofls2idx.keys():
                        bug.write(item[0]+'\t'+item[1]+'\n')
                    bug.close()
                    intent = 0
                    rel = 'L0'
                if intent != 0:
                    rel = 'L'+str(docid2rel[(id,doc)]-1)
                else:
                    rel = 'L0'
                dqrels.write(id+' '+str(intent)+' '+doc+' '+rel+'\n')

dqrels.close()

#############################################################################

runlist = open('../data/flseva/iminerunlist','w')
for f in os.listdir('../data/run'):
    runlist.write(f.replace('txt','run')+'\n')
    runout = open('../data/flseva/'+f.replace('txt','run'),'w')
# 0101 0 clueweb12-0006-97-23810 1 27.73 MSRA-D-E-1A

    for l in open('../data/run/'+f).readlines()[1:]:
        segs = l.strip().replace('&amp;','').split(' ')
        id = segs[0].strip()
        docid  = segs[2].strip()
        docrank = segs[3]
        docscore = segs[4]
        
        runout.write(id+' Q0 '+docid+' '+docrank+' '+docscore+' '+f.replace('.txt','')+'\n')
    runout.close()
runlist.close()
