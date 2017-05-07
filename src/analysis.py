from functools import reduce
import random
import graph

def meanDegree(ppi, proteinlist):
    degDist = list(map(lambda x: len(ppi.Nodes[x].edges), proteinlist))
    meanDeg = reduce(lambda x,y: x + y, degDist) / len(degDist)
    return meanDeg

def nRandProts(n, prots):
    indices = []
    for i in range(0,n):
        r = int(random.uniform(0,len(prots)-1))
        while r in indices:
            r = int(random.uniform(0,len(prots)-1))
        indices.append(r)
    return list(map(lambda x: prots[x], indices))

def getRandItem(items):
    return items[int(random.uniform(0,len(items)-1))]

def switchEdges(g, edges):
    while True:
        e1 = getRandItem(edges)
        e2 = getRandItem(edges)
        #print("Before: E1.frm's neighbors: {0}\ne2.frm's neighbors:{1}"
        #        .format(g[e1.frm].getNeighbors(), g[e2.frm].getNeighbors()))
        if e1 != e2 and e1.frm != e2.frm and e1.to != e2.to:
            e1.to, e2.to = e2.to, e1.to
            return
