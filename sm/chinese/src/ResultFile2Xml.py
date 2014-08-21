#coding=utf8
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from collections import defaultdict
import sys 

from bs4 import BeautifulSoup
reload(sys) 
sys.setdefaultencoding("utf8")
root = Element("root")

child = Element('query',{"id":"0001"})
child.text = '我们'
root.append(child)
tree = ET.ElementTree(root)
tree.write('../data/test.xml','utf8')

# task 1

no2data = defaultdict(lambda:list())
for l in open('../data/csv/task1.csv'):
    segs = l.strip().split(',')
    id = segs[0]
    query = segs[1]
    freqinpool = segs[2]
    relevance = segs[3]
    no2data[id].append((query,freqinpool,relevance))

root = Element("data")
for i in range(1,34,1):
    print i
    if i <10:
        key = '000'+str(i)
    else:
        key = '00'+str(i)
    flsnode = Element('query',{'id':key})
    for item in no2data[key]:
        query = item[0]
        freqinpool = item[1]
        relevance = item[2]
        candnode = Element("candidate",{"content":query,"freqinpool":freqinpool,'relevance':relevance})
        flsnode.append(candnode)
    root.append(flsnode)
tree = ET.ElementTree(root)
tree.write('../data/task1.xml','utf8')
soup = BeautifulSoup(open('../data/task1.xml').read())

open('../data/task1.xml','w').write(soup.prettify())
        

#task2


no2data = defaultdict(lambda:list())
for l in open('../data/csv/task2.csv'):
    segs = l.strip().split(',')
    id = segs[0]
    fls = segs[1]
    sls = segs[2]
    relevance = segs[3]
    no2data[id].append((fls,sls,relevance))

root = Element("data")
for i in range(1,34,1):
    print i
    if i <10:
        key = '000'+str(i)
    else:
        key = '00'+str(i)
    flsnode = Element('query',{'id':key})
    for item in no2data[key]:
        fls = item[0]
        sls = item[1]
        relevance = item[2]
        candnode = Element("candidate",{"firstlevelcandidate":fls,"secondlevelcandidate":sls,'relevance':relevance})
        flsnode.append(candnode)
    root.append(flsnode)
tree = ET.ElementTree(root)
tree.write('../data/task2.xml','utf8')
soup = BeautifulSoup(open('../data/task2.xml').read())

open('../data/task2.xml','w').write(soup.prettify())

#task3


no2data = defaultdict(lambda:list())
for l in open('../data/csv/task3.csv'):
    segs = l.strip().split(',')
    id = segs[0]
    userfls = segs[1]
    markfls = segs[2]
    
    no2data[id].append((userfls,markfls))

root = Element("data")
for i in range(1,34,1):
    print i
    if i <10:
        key = '000'+str(i)
    else:
        key = '00'+str(i)
    flsnode = Element('query',{'id':key})
    for item in no2data[key]:
        userfls = item[0]
        markfls = item[1]
        candnode = Element("candidate",{"user_generate_fls":userfls,"annotated_fls":markfls})
        flsnode.append(candnode)
    root.append(flsnode)
tree = ET.ElementTree(root)
tree.write('../data/task3.xml','utf8')
soup = BeautifulSoup(open('../data/task3.xml').read())

open('../data/task3.xml','w').write(soup.prettify())

#task4
no2data = defaultdict(lambda:list())
for l in open('../data/csv/task4.csv'):
    segs = l.strip().split(',')
    id = segs[0]
    userfls = segs[1]
    markfls = ''
    
    no2data[id].append((userfls,markfls))

root = Element("data")
for i in range(1,34,1):
    print i
    if i <10:
        key = '000'+str(i)
    else:
        key = '00'+str(i)
    flsnode = Element('query',{'id':key})
    for item in no2data[key]:
        userfls = item[0]
        markfls = item[1]
        candnode = Element("candidate",{"content":userfls})
        flsnode.append(candnode)
    root.append(flsnode)
tree = ET.ElementTree(root)
tree.write('../data/task4.xml','utf8')
soup = BeautifulSoup(open('../data/task4.xml').read())

open('../data/task4.xml','w').write(soup.prettify())

# task 5

no2data = defaultdict(lambda:list())
for l in open('../data/csv/task5.csv'):
    segs = l.strip().split(',')
    id = segs[0]
    if len(id) == 1:
        id = '000'+id
    if len(id) ==2:
        id = '00'+id
    
    sls = segs[1]
    freqinpool = segs[2]
    fls_mark = segs[3]
    
    no2data[id].append((sls,freqinpool,fls_mark))

root = Element("data")
for i in range(1,34,1):
    print i
    if i <10:
        key = '000'+str(i)
    else:
        key = '00'+str(i)
    flsnode = Element('query',{'id':key})
    for item in no2data[key]:
        s1 = item[0]
        s2 = item[1]
        s3 = item[2]
        candnode = Element("candidate",{"user_generate_sls":s1,"freqinpool":s2,'annotated_fls':s3})
        
        flsnode.append(candnode)
    root.append(flsnode)
tree = ET.ElementTree(root)
tree.write('../data/task5.xml','utf8')
soup = BeautifulSoup(open('../data/task5.xml').read())

open('../data/task5.xml','w').write(soup.prettify())
        
        

# task 6
no2data = defaultdict(lambda:list())
for l in open('../data/csv/task6.csv'):
    segs = l.strip().split(',')
    id = segs[0]
    if len(id) == 1:
        id = '000'+id
    if len(id) ==2:
        id = '00'+id
    
    sls = segs[1]
    freqinpool = segs[2]
    fls_mark = segs[3]
    sls_mark = segs[4]
    
    no2data[id].append((sls,freqinpool,fls_mark,sls_mark))

root = Element("data")
for i in range(1,34,1):
    print i
    if i <10:
        key = '000'+str(i)
    else:
        key = '00'+str(i)
    flsnode = Element('query',{'id':key})
    for item in no2data[key]:
        s1 = item[0]
        s2 = item[1]
        s3 = item[2]
        s4 = item[3]
        
        candnode = Element("candidate",{"user_generate_sls":s1,"freqinpool":s2,'annotated_fls':s3,'annotated_sls':s4})
        
        flsnode.append(candnode)
    root.append(flsnode)
tree = ET.ElementTree(root)
tree.write('../data/task6.xml','utf8')
soup = BeautifulSoup(open('../data/task6.xml').read())

open('../data/task6.xml','w').write(soup.prettify())

# task 7
no2data = defaultdict(lambda:list())
topiccount  = 1 
innercount = 1
for l in open('../data/csv/task7.csv'):
    if l.strip().split(',')[0] == '':
        topiccount +=1
        innercount =1
        continue
    if len(str(topiccount)) ==1:
        key = '000'+str(topiccount)
    else:
        key = '00'+str(topiccount)
    
    segs = l.strip().split(',')
    sls  = segs[0]
    vote1 = segs[1]
    vote2 = segs[2]
    vote3 = segs[3]
    votesum = segs[4]
    no2data[key].append((str(innercount),sls,vote1,vote2,vote3,votesum))
    innercount +=1
root = Element("data")
for i in range(1,34,1):
    print i
    if i <10:
        key = '000'+str(i)
    else:
        key = '00'+str(i)
    flsnode = Element('query',{'id':key})
    for item in no2data[key]:
        rank = item[0]
        sls = item[1]
        vote1 = item[2]
        vote2 = item[3]
        vote3 = item[4]
        votesum = item[5]
        
        candnode = Element("candidate",{"rank":rank,"annotated_sls":sls,'vote1':vote1,'vote2':vote2,'vote3':vote3,'votesum':votesum})
        
        flsnode.append(candnode)
    root.append(flsnode)
tree = ET.ElementTree(root)
tree.write('../data/task7.xml','utf8')
soup = BeautifulSoup(open('../data/task7.xml').read())

open('../data/task7.xml','w').write(soup.prettify())
