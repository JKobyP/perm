import analysis

def readKinase(filename):
    f = open(filename, 'r')
    o = f.readlines()
    kinase = []
    for line in o:
        line = line.split("\t")
        name = line[1].strip()
        kinase.append(name)
    return kinase

def analyzeKinase(kinasefile,ppiGraph, permutations):
    print("Reading Kinase list: {0}...".format(kinasefile))
    kinaseList = readKinase(kinasefile)
    print("Read kinase list of length: {0}".format(len(kinaseList)))

    print("Finding intersection...")
    kinaseList = list(filter(lambda x: x in ppiGraph,kinaseList))
    print("Left with {0} kinases".format(len(kinaseList)))

    lsize = len(kinaseList)
    deg = analysis.meanDegree(ppiGraph, kinaseList)
    print("Mean degree for Kinase: %.3f" % deg)

    proteins = list(ppiGraph.Nodes.keys())
    for i in range(0,permutations):
        plist = analysis.nRandProts(lsize, proteins)
        deg = analysis.meanDegree(ppiGraph, plist)
        print("Mean degree for random list %d: %.3f" % (i, deg))


