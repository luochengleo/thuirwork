#coding=utf8
count  = 1
fout = open('../data/csv/task7new.csv','w')
for l in open('../data/csv/task7new.txt'):
    
    segs = l.strip().split('\t')
    if segs[0] == '':
        count +=1
    else:
        if count <10:
            id = '000'+str(count)
        else:
            id = '00'+str(count)
        fout.write(','.join([id,','.join(segs)])+'\n')
fout.close()