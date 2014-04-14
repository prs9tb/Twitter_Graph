'''
Program     : Graphs Analyzer
Version     : 1 (Released April 17 2012)
Author      : Mohammed Alenazi
Contact     : malenazi@ittc.ku.edu
Last update : April 17 2012 
Description : To analyze a number of adjacency matrices inputed as text files. 
Usage       : python graphs_analyzer.py

Input : the input files must be in a saperate folder e.g "data"
Sample input :
0 1 0
1 0 0
0 0 0
* note that the delimiter is a space and could be changed by modifying the code

issues:

Given graph G, print:

adjacency_matrix
incidence_matrix
laplacian_matrix
normalized_laplacian_matrix

1- adjacency and laplacian spectrum values should be rounded to 4 decimal points >>> round(2.6751, 4)
2- sort all adjacency_spectrum values
3- sort all laplacian_spectrum values
4- print top 5 max and min values
5- print or not         print "normalized_laplacian_matrix",'\t\t\t\n', nx.normalized_laplacian_matrix(graphs[g])
6- print *normalized laplacian spectrum*

7- print CDF of normalized laplacian spectrum  (cdf conversion example is:  http://www.srcco.de/v/cdf-plots-perf-eval)

'''

import networkx as nx
import os
import csv
import numpy
import statistics
from networkx.algorithms import bipartite


# you can change the target folder here
dir_list =  os.listdir("data")
new_dir_list = []
for item in dir_list:
    if item[0]!=".":
        new_dir_list.append(item)
dir_list = new_dir_list

def get_avg(temp):
    values = temp.values()
    size = len(temp)
    total = float(sum(values))
    min_value = min (values)
    max_value = max (values)
    average = total / size
    return round(min_value,4),round(average,4),round(max_value,4)

def get_max(param):
    param1 = numpy.real(param)
    temp = [round(x, 4) for x in param1]
    temp.sort()
    if len(temp) > 5:
        return temp[-5:]
    else:
        return temp

def get_min(param):
    param1 = numpy.real(param)
    temp = [round(x, 4) for x in param1]
    temp.sort()
    if len(temp) > 5:
        return temp[0:5]
    else:
        return temp
        
def normalized_laplacian_spectrum(G, weight='weight'):
    try:
        import numpy as np
    except ImportError:
        raise ImportError(
        "laplacian_spectrum() requires NumPy: http://scipy.org/ ")
    return np.linalg.eigvals(nx.normalized_laplacian(G,weight=weight))

print "The files to be read ", dir_list
graphs = {}
'''
Reading all the files and storing them in a dictionary
'''
for item in dir_list:
    print "Reading", item
    f = open('data/'+item,'r')
    f = csv.reader(open('data/'+item,'r'), delimiter=' ', quotechar='"')
    lines= list(f)
    g = nx.Graph()
    #g = nx.DiGraph()
    g.add_nodes_from(range(len(lines)))
    for row in range(len(lines)):
        for col in range(len(lines)):
            if int(lines[row][col]) == 1:
                g.add_edge(row,col)
    print "Done reading all the files"  
    graphs[item] = g


for g in graphs.keys():
    try:
        print "====================== " , g, "==========================="
        print "number of isolated nodes",'\t\t\t',nx.isolates(graphs[g])
        print "is graph biconnected?",'\t\t\t',nx.is_biconnected(graphs[g])
        print "cut vertices are: ",'\t\t\t',list(nx.articulation_points(graphs[g]))
        print "number of nodes",'\t\t\t',len(graphs[g].nodes())
        print "number of edges",'\t\t\t',len(graphs[g].edges())
        print "degree",'\t\t\t',get_avg(graphs[g].degree())
        print "diameter",'\t\t\t', nx.diameter(graphs[g])
        print "radius",'\t\t\t', nx.radius(graphs[g])
        print "is_bipartite?",'\t\t', bipartite.is_bipartite(graphs[g])
        print "average_shortest_path_length",'\t\t', nx.average_shortest_path_length(graphs[g])
        print "degree_assortativity_coefficient",'\t\t', nx.degree_assortativity_coefficient(graphs[g])
        print "assortativity.average_degree_connectivity",'\t\t', nx.assortativity.average_degree_connectivity(graphs[g])
        #print "degree_pearson_correlation_coefficient",'\t\t', nx.degree_pearson_correlation_coefficient(graphs[g])
        print "node closeness_centrality",'\t\t\t', get_avg(nx.closeness_centrality(graphs[g]))
        print "clustering",'\t\t\t', get_avg(nx.clustering(graphs[g]))
        print "node betweeness",'\t\t\t', get_avg(nx.betweenness_centrality(graphs[g],normalized=False,endpoints=False))
        print "edge betweeness",'\t\t\t', get_avg(nx.edge_betweenness_centrality(graphs[g],normalized=False))
        #print "spectral_bipartivity",'\t\t', bipartite.spectral_bipartivity(graphs[g])
        #print "node betweeness normalized",'\t\t\t', get_avg(nx.betweenness_centrality(graphs[g],normalized=True,endpoints=False))
        #print "edge betweeness normalized",'\t\t\t', get_avg(nx.edge_betweenness_centrality(graphs[g],normalized=True))
        #print "node closeness_vitality",'\t\t\t', get_avg(nx.closeness_vitality(graphs[g]))
        #print "communicability_centrality",'\t\t', get_avg(nx.communicability_centrality(graphs[g]))
        #print "communicability_betweenness_centrality",'\t\t', get_avg(nx.communicability_betweenness_centrality(graphs[g]))
        #print "transitivity",'\t\t\t', round(nx.transitivity(graphs[g]),4)
        #print "laplacian_spectrum",'\t\t\n:', nx.laplacian_spectrum(graphs[g])
        print "adjacency_spectrum",'\t\tMin 5 :', get_min(nx.adjacency_spectrum(graphs[g])) , "\t\tMax 5 :",get_max(nx.adjacency_spectrum(graphs[g]))
        print "laplacian_spectrum",'\t\tMin 5 :', get_min(nx.laplacian_spectrum(graphs[g])) , "\t\tMax 5 :",get_max(nx.laplacian_spectrum(graphs[g])) 
        #print "normalized_laplacian_spectrum",'\t\tMin 5 :', get_min(numpy.real(normalized_laplacian_spectrum(graphs[g]))) , "\t\tMax 5 :",get_max(normalized_laplacian_spectrum(graphs[g]))
        #print "adjacency_spectrum",'\t\t\n', nx.adjacency_spectrum(graphs[g])
        #print "laplacian_spectrum",'\t\t\n', nx.laplacian_spectrum(graphs[g])
        #print "normalized_laplacian_spectrum",'\t\t\n', normalized_laplacian_spectrum(graphs[g])
        ####print "adjacency_spectrum",'\t\t\n', numpy.around(numpy.real(nx.adjacency_spectrum(graphs[g])), decimals=4)
        ####print "laplacian_spectrum",'\t\t\n', numpy.around(numpy.real(nx.laplacian_spectrum(graphs[g])), decimals=4)
        ####print "normalized_laplacian_spectrum",'\t\t\n', numpy.around(numpy.real(normalized_laplacian_spectrum(graphs[g])), decimals=4)
        #statistics.pdf_to_textfile(numpy.real(numpy.around(nx.adjacency_spectrum(graphs[g]), decimals=2)).tolist(),g+"_adj_pdf.txt")
        # Write to a file
        #statistics.to_textfile(numpy.real(numpy.around(nx.adjacency_spectrum(graphs[g]), decimals=2)).tolist(),g+"_adj_pdf.txt")
        #statistics.pdf_to_textfile(numpy.real(numpy.around(nx.laplacian_spectrum(graphs[g]), decimals=2)).tolist(),g+"_pdf.txt")
        #statistics.cdf_to_textfile(numpy.real(numpy.around(nx.laplacian_spectrum(graphs[g]), decimals=2)).tolist(),g+"_cdf.txt")
        #statistics.pdf_to_textfile(numpy.real(numpy.around(normalized_laplacian_spectrum(graphs[g]), decimals=4)).tolist(),g+"_pdf.txt")
        #statistics.cdf_to_textfile(numpy.real(numpy.around(normalized_laplacian_spectrum(graphs[g]), decimals=4)).tolist(),g+"_cdf.txt")
        #print "adjacency_matrix",'\t\t\t\n', nx.adjacency_matrix(graphs[g])
        #print "laplacian_matrix",'\t\t\t\n', nx.laplacian_matrix(graphs[g])
        #print "normalized_laplacian_matrix",'\t\t\t\n', nx.normalized_laplacian(graphs[g])
        #print "connected_component_subgraphs",'\t\t\t', nx.connected_component_subgraphs(graphs[g])
        #print "eigenvector_centrality",'\t\t', get_avg(nx.eigenvector_centrality(graphs[g]))
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    except(ImportError):
        print 'Error'


