#coding=utf8
import os
import sys
dir = sys.argv[1]
cutoff = sys.argv[2]
outfile = sys.argv[3]
fout = open(outfile,'w')

for f in os.listdir(dir):
    Dsharpsum = 0.0
    Dsharpcount = 0.0
    IRelnsum = 0.0
    IRelncount = 0.0
    
    IRel50sum = 0.0
    IRel50count = 0.0
    for l in open(dir+'/'+f):
        segs = l.strip().split(' ')
        if segs[1] == 'nDCG@'+cutoff+'=':
            for item in segs[2:]:
                if item != '':
                    Dsharpsum += float(item)
                    
            Dsharpcount +=1
        if segs[1] == 'I-rec@n=':
            for item in segs[2:]:
                if item != '':
                    IRelnsum += float(item)
            IRelncount +=1
        if segs[1] == 'I-rec@'+cutoff+'=':
            for item in segs[2:]:
                if item != '':
                    IRel50sum += float(item)
            IRel50count +=1
    
    print f.split('.')[0],'\t',Dsharpsum,'\t',Dsharpcount,'\t', IRelnsum,'\t',IRelncount,'\t',IRel50sum,'\t',IRel50count
    outfile.write(f.split('.')[0]+','+str(Dsharpsum)+","+str(Dsharpcount)+','+str(IRelnsum)+','+str(IRelncount)+','+str(IRel50sum)+','+str(IRel50count)+'\n')
outfile.close()    