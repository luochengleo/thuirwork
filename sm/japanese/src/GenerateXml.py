#coding=utf8
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from collections import defaultdict
import sys,csv 
import codecs

from bs4 import BeautifulSoup
reload(sys) 
sys.setdefaultencoding("utf8")

def loadcsv(filename):
    return csv.reader(open(filename))
id2topic = dict()
for l in open('../data/temp/IMine.Query.txt').readlines():
    id,topic = l.replace(codecs.BOM_UTF8,'').strip().split('\t')
    id2topic[id] = topic
    print id,topic
def evaid():
    rtr = []
    for i in range(101,150,1):
        if i <10:
            rtr.append('000'+str(i))
        if i>=10 and i<100:
            rtr.append('00'+str(i))
        if i >=100:
            rtr.append('0'+str(i))
    return rtr
sls2id = dict()
for l in open('../data/temp/slsposs.txt').readlines():
    segs = l.strip().split('\t')
    sls2id[segs[1]] = segs[0]
id2fls2sls2queries = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:set())))

idannofls2userfls = defaultdict(lambda:list())
for l in loadcsv('../data/csv/task3.csv'):
    id = l[0]
    userfls = l[1]
    annofls = l[2]
    
    idannofls2userfls[(id,annofls)].append(userfls)

for l in loadcsv('../data/csv/task6.csv'):
    query = l[1]
    fls = l[3]
    sls = l[4]
    if sls in sls2id:
        if query != '' and fls != '' and sls != '':
            id  = sls2id[sls]
            id2fls2sls2queries[id][fls][sls].add(query)

id2fls = defaultdict(lambda:list())
id2flsposs = defaultdict(lambda:dict())
for l in open('../data/temp/flsposs.txt'):
    segs = l.strip().split('\t')
    id = segs[0]
    fls = segs[1]
    poss = float(segs[2])
    id2fls[id].append(fls)
    id2flsposs[id][fls] = poss


id2sls = defaultdict(lambda:list())
id2slsposs = defaultdict(lambda:dict())

for l in open('../data/temp/slsposs.txt'):
    segs = l.strip().split('\t')
    id = segs[0]
    sls = segs[1]
    poss = float(segs[2])
    id2sls[id].append(sls)
    id2slsposs[id][sls] = poss


for l in open('../data/temp/flsposs.txt'):
    segs = ''

root =  ET.Element('root')
for id in evaid():
    topic  = id2topic[id]
    topicnode = ET.Element('topic',{'id':id,'content':topic})
    
    for fls in id2fls[id]:
        print id,fls
        flsnode = ET.Element('fls',{'content':fls,'poss':str(id2flsposs[id][fls])})
        examplesnode = ET.Element('examples')
        for item in idannofls2userfls[(id,fls)]:
            flsexpnode = ET.Element('example')
            flsexpnode.text = item
            examplesnode.append(flsexpnode)
        flsnode.append(examplesnode)
        for sls in id2sls[id]:
            if sls in id2fls2sls2queries[id][fls]:
                slsnode = ET.Element('sls',{'content':sls,'poss':str(id2slsposs[id][sls])})
                for q in id2fls2sls2queries[id][fls][sls]:
                    expnode = ET.Element('example')
                    expnode.text = q
                    slsnode.append(expnode)
                flsnode.append(slsnode)
        
        topicnode.append(flsnode)
    root.append(topicnode)

tree = ET.ElementTree(root)
tree.write('../data/IMine.Qrel.SMJ.xml','utf8')
