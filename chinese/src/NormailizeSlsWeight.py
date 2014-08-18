#coding=utf8
import csv
def loadcsv(filename):
    return csv.reader(open(filename))

def sort_by_value(d):
    items = d.items()
    backitems = [[v[1] , v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[i][1] for i in range(0,len(backitems))]

from  collections import defaultdict

id2sum =defaultdict(lambda: 0)
def evaid():
    rtr = []
    for i in range(1,34,1):
        if i <10:
            rtr.append('000'+str(i))
        else:
            rtr.append('00'+str(i))
    return rtr
for l in loadcsv('../data/csv/task7new.csv'):
    id = l[0]
    annosls = l[1]
    weight = l[5]
    id2sum[id]+= int(weight)

id2sls2poss = defaultdict(lambda : dict())
for l in loadcsv('../data/csv/task7new.csv'):
    id = l[0]
    annosls = l[1]
    weight = l[5]
    id2sls2poss[id][annosls] = float(int(weight))/float(id2sum[id])

fout = open('../data/temp/slsposs.txt','w')
for id in evaid():
    print id
    for item in sort_by_value(id2sls2poss[id]):
        fout.write(id+'\t'+item+'\t'+str(id2sls2poss[id][item])+'\n')

fout.close()