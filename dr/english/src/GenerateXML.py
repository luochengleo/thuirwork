#coding=utf8
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from collections import defaultdict
import sys,csv 
import codecs
query2id = dict()
for l in open('../data/temp/IMine.Query.txt'):
    id,query = l.strip().split('\t')
    query2id[query] =  id
def loadcsv(filename):
    return csv.reader(open(filename))


data= ET.Element("data")
comment = ET.Element("comment")
comment.text = "The annotations contain two parts: one is relevance judgments and the other is document relevance with the subtopics."
data.append(comment)
comment = ET.Element("comment")
comment.text = "In relevance judgment: 0 means unaccessable link; 1 means irrelevant; 2 means relevant and 3 means very relevant"
data.append(comment)
relevance = ET.Element("relevance")
for l in loadcsv('../data/csv/dr1.csv'):
    query = l[0]
    docid = l[1]
    rel = l[2]
    try:
        queryid = query2id[query]
    except:
        if query[0] =='m':
            queryid=='0092'
        else:
            queryid = '0100'
    doc = ET.Element("doc",{"docid":docid,'queryid':queryid,"relevance":rel})
    relevance.append(doc)
data.append(relevance)
relevance = ET.Element('relevance')
for l in loadcsv('../data/csv/dr2.csv'):
    query = l[0]
    docid = l[1]
    rel = l[2]
    try:
        queryid = query2id[query]
    except:
        if query[0] =='m':
            queryid=='0092'
        else:
            queryid = '0100'
    for item in l[3:]:
        if item.strip() !='':
            doc = ET.Element('doc',{"docid":docid,'queryid':queryid,'relevance':rel,'sls':item.strip()})
            relevance.append(doc)
data.append(relevance)
tree = ET.ElementTree(data)
tree.write('../data/IMine.Qrel.DRE.xml','utf8')
    
