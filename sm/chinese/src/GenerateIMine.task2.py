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
for l in loadcsv("../data/csv/task2new.csv"):
    queryid = l[0]
    userfls = l[1]
    usersls = l[2]
    rel = l[4]
    anno = ET.Element("annotation",{'queryid':queryid,"user_fls":userfls,"user_sls":usersls,"relevance":rel})
    root.append(anno)
tree= ET.ElementTree(root)
tree.write('../data/IMine.Qrel.SMC.Hierarchy.xml')