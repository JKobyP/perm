#!/bin/python3

import graph
import kinase
import analysis
import disease
import modularity
from optparse import OptionParser

def readPPI(filename, thresh):
    f = open(filename, 'r')
    o = f.readlines()
    return parsePPI(o, thresh), o

def parsePPI(o, thresh):
    g = graph.Graph()
    for line1 in o:
        line = line1.split("\t")
        frm = line[0].strip()
        to = line[2].strip()
        score = float(line[4])
        if frm == to:
            continue
        g.add_node(frm)
        # sometimes the "to" column has a comma-separated list
        if ',' in to:
            for n in to.split(','):
                g.add_node(n.strip())
                if score > thresh:
                    g.add_edge(frm, n, w=thresh)
        else:
            g.add_node(to)
            if score > thresh:
                g.add_edge(frm, to, w=thresh)
    return g

def main():
    parser = OptionParser()
    parser.add_option("-p", "--ppifile", dest="ppifile",
                  help="The file containing the hippie ppi network", metavar="FILE")
    parser.add_option("-t", "--threshold", dest="threshold", default=.5,
                  help="The cutoff threshold for the hippie network (0.0-1.0)",
                  metavar="NUM")
    parser.add_option("-n", "--permutations", dest="permutations", default=30,
                  help="The number of permutations for each permutation test",
                  metavar="NUM")
    parser.add_option("-f", "--kinasefile", dest="kinasefile",
                  help="The file containing the kinase list", metavar="FILE")
    parser.add_option("-o", "--diseasefolder", dest="diseaseFolder",
                  help="The folder containing the disease files", metavar="FILE")
    parser.add_option("-k", "--kinase",
                  action="store_true", dest="dokinase", default=False,
                  help="do kinase analysis")
    parser.add_option("-d", "--disease",
                  action="store_true", dest="dodisease", default=False,
                  help="do disease analysis")
    parser.add_option("-m", "--module",
                  action="store_true", dest="domodule", default=False,
                  help="do module analysis")
    (options, args) = parser.parse_args()

    ppifile = options.ppifile
    threshold = float(options.threshold)
    kinasefile = options.kinasefile
    diseaseFolder = options.diseaseFolder
    permutations = int(options.permutations)
    print("Reading PPI graph: {0}...".format(ppifile))
    ppiGraph, out = readPPI(ppifile,threshold)
    print("Read in {0} nodes".format(len(ppiGraph.Nodes)))

    if options.dokinase:
        print("\n---------- Analyzing Kinase ----------")
        kinase.analyzeKinase(kinasefile, ppiGraph, permutations)

    if options.dodisease or options.domodule:
        print("\n--------- Analyzing Diseases ---------")
        mngraphs, randgraphs = disease.analyzeDisease(diseaseFolder, ppiGraph, permutations)
    if options.domodule:
        print("\n-------- Analyzing Modularity --------")
        modularity.analyzeModularity(ppiGraph, mngraphs, randgraphs, permutations)

if __name__ == "__main__":
    main()
