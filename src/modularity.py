import analysis

def analyzeModularity(ppi, mngraphs, randgraphs, p):
    tri = analysis.countTriangles(ppi)
    print("PPI has triangles at a frequency of %.3f" % tri)
    for g in mngraphs:
        tri = analysis.countTriangles(g)
        print("MN graph has triangles at a frequency of %.3f" % tri)
    for g in randgraphs:
        tri = analysis.countTriangles(g)
        print("Random graph has triangles at a frequency of %.3f" % tri)
