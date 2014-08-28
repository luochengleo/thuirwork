from collections import defaultdict

def getQueryType(queryid):
    if queryid <118:
        return 0
    if queryid >=118 and queryid <135:
        return 1
    if queryid >=135:
        return 2

run2hscore = defaultdict(lambda: 0.0)
run2fscore = defaultdict(lambda: 0.0)
run2sscore = defaultdict(lambda: 0.0)
run2hmeasure = defaultdict(lambda: 0.0)

pertopicout = open('jp.final.pertopic.csv','w')

for l in open('jp.pertopic.csv').readlines()[1:]:
    segs = l.strip().split(',')
    runname = segs[0]
    queryid = int(segs[1])
    fscore = float(segs[3])
    sscore = float(segs[6])
    hscore = float(segs[8])
    
    run2hscore[runname]+=hscore
    if getQueryType(queryid)==0:
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
    allout.write(r+','+str(run2hscore[r]/34.0)+','+str(run2fscore[r]/17.0))
    allout.write(','+str(run2sscore[r]/34.0)+','+str(run2hmeasure[r]/34.0)+'\n')
allout.close()