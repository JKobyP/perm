import analysis
import os
import glob
import graph
import time

mnGraphs = []
randGraphs = []

def readDiseases(folder):
    nameglob = os.path.join(folder,"*.tab")
    files = glob.glob(nameglob)
    diseases = {}
    for filename in files:
        print("Reading %s..." % filename)
        f = open(filename, 'r')
        o = f.readlines()
        proteins = []
        for line in o:
            line = line.split("\t")
            name = line[3].strip()
            proteins.append(name)
        diseases[filename] = proteins
    return diseases

def analyzeDisease(folder, ppiGraph, permutations):
    print("Reading disease lists: %s..." % folder)
    diseases = readDiseases(folder) 
    # Only consider disease proteins our graph knows about
    for disease, proteins in diseases.items():
        diseases[disease] = list(filter(lambda x: x in ppiGraph, proteins))

    # for each disease, compare connectedness with p random protein sets
    for disease, proteins in diseases.items():
        print("\n* Analyzing disease %s (%d proteins)..." % (disease, len(proteins)))
        numConnections = countConnections(proteins, ppiGraph)
        print("\tDisease %s has %d interactions between its own proteins" %
                (disease, numConnections))
        print("\t 1. Permuting on proteins...")
        for x in range(0,permutations):
            randlist = analysis.nRandProts(len(proteins), list(ppiGraph.Nodes.keys()))
            count = countConnections(randlist, ppiGraph)
            print("\t\tList of random proteins has %d interactions" % count)
    
       # for each disease, compare connectedness in random graphs
        print("\t 2. Permuting on graphs of m by n...")
        for i in range(0, permutations):
            if len(mnGraphs) < permutations:
                mnGraphs.append(generateMNGraph(ppiGraph))
            randgraph = mnGraphs[i]
            count = countConnections(proteins, randgraph)
            print("\t\tRandom graph shows %d interactions for this disease" % count)

        # for each disease, compare connectedness in degree-preserving rand graphs
        print("\t 3. Permuting on graphs, preserving degree distribution")
        for i in range(0, permutations):
            if len(randGraphs) < permutations:
                randGraphs.append(generateRandGraph(ppiGraph))
            rgraph = randGraphs[i]
            count = countConnections(proteins, rgraph)
            print("\t\tRandom graph shows %d interactions for this disease" % count)
    return mnGraphs, randGraphs

def generateMNGraph(ppiGraph):
    print("\tCreating random graph...")
    randgraph = graph.Graph({k: graph.Node(k) for k in
                    ppiGraph.Nodes.keys()})
    start = time.time()
    for j in range(0, ppiGraph.numEdges):
        #if j % 1000 == 0:
           # end = time.time()
           # print("Formed %d edges in %.3f" % (j,(end - start)))
           # start = end
        prots = list(randgraph.Nodes.keys())
        p1 = analysis.getRandItem(prots)
        p2 = analysis.getRandItem(prots)
        while randgraph.has_edge(p1,p2):
            p1 = analysis.getRandItem(prots)
            p2 = analysis.getRandItem(prots)
        randgraph.add_edge(p1,p2)
    return randgraph

def generateRandGraph(ppiGraph):
    rgraph = ppiGraph.copy()
    edges = rgraph.getEdges()
    for x in range(0,2*rgraph.numEdges):
        analysis.switchEdges(rgraph, edges)
    return rgraph

def countConnections(nodes, graph):
    count = 0
    for node in nodes:
        for neighbor in graph.Nodes[node].getNeighbors():
            if neighbor.key in nodes:
                count = count + 1
    return count/2
