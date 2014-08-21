#coding=utf8
import os
import sys
dir = sys.argv[1]
cutoff = sys.argv[2]
outfile = sys.argv[3]
overall = open(outfile,'w')
overall.write('Runname,D#-nDCG@'+str(cutoff)+','+'I-Recall@'+str(cutoff)+',D-nDCG@'+str(cutoff)+'\n')
for f in os.listdir(dir):
    Dsharpsum = 0.0
    Dsharpcount = 0.0
    Dsum = 0.0
    Dcount = 0.0
    
    IRel50sum = 0.0
    IRel50count = 0.0
    for l in open(dir+'/'+f):
        segs = l.strip().split(' ')
        if segs[1] == 'D#-nDCG@'+cutoff+'=':
            for item in segs[2:]:
                if item != '':
                    if float(item )<=1:
                        Dsharpsum += float(item)
                    
            Dsharpcount +=1
        if segs[1] == 'I-rec@'+cutoff+'=':
            for item in segs[2:]:
                if item != '':
                    if float(item )<=1:
                        IRel50sum += float(item)
            IRel50count +=1
        if segs[1] == 'nDCG@'+cutoff+'=':
            for item in segs[2:]:
                if item != '':
                    if float(item )<=1:
                        Dsum += float(item)
            Dcount +=1

    if Dsharpcount==IRel50count and IRel50count==Dcount:
        print Dsharpcount,f
        overall.write(f.split('.')[0]+','+str(Dsharpsum/float(Dsharpcount))+','+str(IRel50sum/float(IRel50count))+','+str((Dsum)/float(Dcount))+'\n')
    else:
        print 'error'
overall.close()    