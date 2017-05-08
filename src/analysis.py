from functools import reduce
import random
import graph

def meanDegree(ppi, proteinlist):
    degDist = list(map(lambda x: len(ppi.Nodes[x].edges), proteinlist))
    meanDeg = reduce(lambda x,y: x + y, degDist) / len(degDist)
    return meanDeg

def nRandProts(n, prots):
    randlist = []
    for i in range(0,n):
        r = random.choice(prots)
        while r in randlist:
            r = random.choice(prots)
        randlist.append(r)
    return randlist

def getRandItem(items):
    return random.choice(items)

def switchEdges(g, edges):
    while True:
        e1 = getRandItem(edges)
        e2 = getRandItem(edges)
        if e1 != e2 and e1.frm != e2.frm and e1.to != e2.to:
            g.remove_edge(e1.frm.key,e1.to.key)
            g.remove_edge(e2.frm.key,e2.to.key)
            g.add_edge(e1.frm.key, e2.to.key)
            g.add_edge(e2.frm.key, e1.to.key)
            return

def countTriangles(graph):
    trials = int(graph.numNodes / 2)
    fails = 0
    for n in nRandProts(trials, graph.getLabels()):
        neighbors = graph.Nodes[n].getNeighbors()
        if len(neighbors) < 2:
            fails += 1
        else:
            e1 = getRandItem(neighbors)
            e2 = e1
            ctr = 0
            while e2 == e1:
                ctr += 1
                if ctr > 5:
                    break
                e2 = getRandItem(neighbors)
            if e1 not in e2.getNeighbors():
                fails += 1
    return (trials - fails) / trials
