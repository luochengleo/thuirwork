from collections import defaultdict

tag = 'en'
querynum = 33.0
ambiquerynum = 16.0

def getQueryType(queryid):
    if queryid <67:
        return 0
    else:
        return 1

run2hscore = defaultdict(lambda: 0.0)
run2fscore = defaultdict(lambda: 0.0)
run2sscore = defaultdict(lambda: 0.0)
run2hmeasure = defaultdict(lambda: 0.0)



pertopicout = open(tag+'.release.pertopic.csv','w')
pertopicout.write('queryid,topicid,Fscore:D-nDCG@5,Fscore:D#nDCG@5,FscoreI-rel@5,Sscore:D-nDCG@50,Fscore:D#nDCG@50,FscoreI-rel@50,Hscore,Hmeasure\n')
print 'read pertopic data'

for l in open(tag+'.pertopic.csv').read().split('\n')[2:]:
    print l
    segs = l.strip().split(',')
    runname = segs[0]
    queryid = int(segs[1])
    fscore = float(segs[3])
    sscore = float(segs[6])
    hscore = float(segs[8])
    
    run2hscore[runname]+=hscore
    
    run2sscore[runname]+=sscore
    
    if getQueryType(queryid) == 0:
        run2fscore[runname]+=fscore
        hmeasure = hscore*(fscore+sscore)/2.0
    else:
        hmeasure = hscore*sscore
    run2hmeasure[runname]+= hmeasure
    pertopicout.write(l.strip()+','+str(hmeasure)+'\n')

pertopicout.close()
allout = open(tag+'.release.perrun.csv','w')
allout.write('runname,h-score,f-score,s-score,h-measure\n')
for r in sorted(list(run2hscore.keys())):
    allout.write(r+','+str(run2hscore[r]/querynum)+','+str(run2fscore[r]/ambiquerynum))
    allout.write(','+str(run2sscore[r]/querynum)+','+str(run2hmeasure[r]/querynum)+'\n')
allout.close()