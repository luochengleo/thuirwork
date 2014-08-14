#coding=utf8
import os
for f in os.listdir('../data/Dqrels/sakai/Dnev/'):
    Dsharpsum = 0.0
    Dsharpcount = 0.0
    IRelnsum = 0.0
    IRelncount = 0.0
    
    IRel50sum = 0.0
    IRel50count = 0.0

    for l in open('../data/Dqrels/sakai/Dnev/'+f):
        segs = l.strip().split(' ')
        if segs[1] == 'nDCG@0050=':
            for item in segs[2:]:
                if item != '':
                    Dsharpsum += float(item)
                    
            Dsharpcount +=1
        if segs[1] == 'I-rec@n=':
            for item in segs[2:]:
                if item != '':
                    IRelnsum += float(item)
            IRelncount +=1
        if segs[1] == 'I-rec@50=':
            for item in segs[2:]:
                if item != '':
                    IRel50sum += float(item)
            IRel50count +=1
    print f.split('.')[0],'\t',Dsharpsum,'\t',Dsharpcount,'\t', IRelnsum,'\t',IRelncount,'\t',IRel50sum,'\t',IRel50count     