#coding=utf8
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from collections import defaultdict
import sys,csv 
import codecs
reload(sys) 
sys.setdefaultencoding("utf8")
def loadcsv(filename):
    return csv.reader(open(filename))
root = ET.Element("data")
for l in loadcsv("../data/csv/task2.new.csv"):
    queryid ='00'+ l[0].decode('utf8','ignore').encode('utf8')
    
    userfls = l[1].decode('utf8','ignore').encode('utf8')
    usersls = l[2].decode('utf8','ignore').encode('utf8')
    rel = l[3].decode('utf8','ignore').encode('utf8')
    anno = ET.Element("annotation",{'queryid':queryid,"user_fls":userfls,"user_sls":usersls,"relevance":rel})
    root.append(anno)
tree= ET.ElementTree(root)
tree.write('../data/IMine.Qrel.SME.Hierarchy.xml')