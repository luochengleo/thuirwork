#coding=utf8

fout = open('../data/csv/task3.csv','w')
for l in open('../data/flscluster.csv').readlines()[1:]:
    segs = l.strip().split('\t')
    id = '0'+segs[0]
    annofls = segs[4]
    userflses = segs[5].split(',')
    for item in userflses:
        if item !='':
            fout.write(id+','+item+','+annofls+'\n')
fout.close()