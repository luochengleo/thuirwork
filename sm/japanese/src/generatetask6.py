#coding=utf8
import bs4
import sys
reload(sys) 
sys.setdefaultencoding("utf8")

from bs4 import BeautifulSoup
flsp = open('../data/temp/flsposs.txt','w')
slsp = open('../data/temp/slsposs.txt','w')
flspossalready = set()
soup = BeautifulSoup(open('../data/IMine.Qrel.SMJ.xml'))
root = soup.find('root')
task6 = open('../data/csv/task6.csv','w')
for topicnode in root.children:
    if type(topicnode) == bs4.element.Tag:
        topicid = topicnode['id']
        
        for flsnode in topicnode.children:
            if type(flsnode) == bs4.element.Tag:
                flsposs = flsnode['poss']
                flscontent = flsnode['content']
                if (topicid,flscontent,flsposs) not in flspossalready:
                    flsp.write(topicid+'\t'+flscontent+'\t'+flsposs+'\n')
                    flspossalready.add((topicid,flscontent,flsposs))
                for slsnode in flsnode.children:
                    if type(slsnode) == bs4.element.Tag:
                        slsposs = slsnode['poss']
                        slscontent = slsnode['content']
                        slsp.write(topicid+'\t'+slscontent+'\t'+slsposs+'\n')
                        for slsexpnode in slsnode.children:
                            if type( slsexpnode) == bs4.element.Tag:
                                print slsexpnode.string
                                task6.write('1,'+slsexpnode.string+','+'13,'+flscontent+','+slscontent+'\n')
flsp.close()
slsp.close()
task6.close()