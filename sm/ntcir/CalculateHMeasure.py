from collections import defaultdict

def getQueryType(queryid):
    if queryid <118:
        return 0
    else:
        return 1

run2hscore = defaultdict(lambda: 0.0)
run2fscore = defaultdict(lambda: 0.0)
run2sscore = defaultdict(lambda: 0.0)
run2hmeasure = defaultdict(lambda: 0.0)

pertopicout = open('jp.final.pertopic.csv','w')
print 'read pertopic data'

for l in open('jp.pertopic.csv').read().split('\n')[2:]:
    print l
    segs = l.strip().split(',')
    runname = segs[0]
    queryid = int(segs[1])
    fscore = float(segs[3])
    sscore = float(segs[6])
    hscore = float(segs[8])
    
    run2hscore[runname]+=hscore
    run2fscore[runname]+=fscore
    run2sscore[runname]+=sscore
    
    if getQueryType(queryid) == 0:
        hmeasure = hscore*(fscore+sscore)/2.0
    else:
        hmeasure = hscore*sscore
    run2hmeasure[runname]+= hmeasure
    pertopicout.write(l.strip()+','+str(hmeasure)+'\n')

pertopicout.close()
allout = open('jp.final.perrun.csv','w')
allout.write('runname,h-score,f-score,s-score,h-measure\n')
for r in sorted(list(run2hscore.keys())):
    allout.write(r+','+str(run2hscore[r]/33.0)+','+str(run2fscore[r]/33.0))
    allout.write(','+str(run2sscore[r]/33.0)+','+str(run2hmeasure[r]/33.0)+'\n')
allout.close()