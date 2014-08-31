#coding=utf8
import sys,csv 
import codecs
from collections import defaultdict
reload(sys) 
sys.setdefaultencoding("utf8")
smfile = 'IMine.Qrel.SMC.xml'
drfile = 'IMine.Qrel.DRC.xml'
import xml.etree.ElementTree as ET

from xml.etree.ElementTree import XMLParser
def sls2fls(sls):
    segs = sls.strip().split('_')
    if len(segs)==2:
        return segs[0]
    if len(segs)==3:
        return segs[0]+'_'+segs[1]
id2fls2sls = defaultdict(lambda:defaultdict(lambda:set()))
parser = XMLParser(encoding="utf-8")
tree = ET.parse('../data/'+smfile, parser=parser)
root = tree.getroot()
for topic in root:
    queryid =topic.get('id')
    query = topic.get('content')
    for fls in topic:
        flscontent = fls.get('content')
        for sls in fls:
            if sls.tag =='sls':
                slscontent = sls.get("content")
                id2fls2sls[queryid][flscontent].add(slscontent)
                if (flscontent in slscontent) == False:
                    print flscontent,slscontent
parser = XMLParser(encoding="utf-8")
tree =ET.parse('../data/'+drfile,parser=parser)
root = tree.getroot()
for doc in root[3]:
    docid = doc.get('docid')
    queryid = doc.get('queryid')
    sls = doc.get('sls')
    fls = sls2fls(sls)
    if fls not in id2fls2sls[queryid]:
        print 'miss fls',queryid,fls,id2fls2sls[queryid]
    if sls not in id2fls2sls[queryid][fls]:
        print 'miss sls',queryid,sls
    