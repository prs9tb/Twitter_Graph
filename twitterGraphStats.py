import networkx as nx
import os
import openpyxl as xl
import numpy as np
import statistics
from networkx.algorithms import bipartite

def __main__():
	os.chdir("C:\Users\prs9tb\Documents\GitHub\Twitter_Graph")
	print "enter twitter data xlsx (Excel) file:"
	filepath = raw_input().strip()
	if filepath[-5:] != '.xlsx':
		filepath += '.xlsx'
	print "reading:", filepath
	workbook = xl.load_workbook(filename = filepath) ##workbook
	
	sheetNames = workbook.get_sheet_names()
	print "Sheets: ", sheetNames
	
	
	twitterIDs = {}
	dg = nx.DiGraph() ## creating a directed graph
	
	ws = workbook.get_sheet_by_name(sheetNames[0])
	print 'reading id sheet:', ws.title, "...",
	for row in ws.rows[1:]:
		id = row[0].value
		name = row[2].value
		twitterIDs[id] = name
		dg.add_node(id)
	print "done!"
	
	ws = workbook.get_sheet_by_name(sheetNames[1])
	print 'reading relationship sheet:', ws.title, "...",
	for row in ws.rows[1:]:
		source = row[0].value
		dest = row[1].value
		edge = row[4].value
		if edge:
			sToD = row[2]
			dToS = row[3]
			if sToD:
				dg.add_edge(source, dest)
			if dToS:
				dg.add_edge(dest, source)
	print "done!"
	
	print "Number of nodes/edges: ", dg.number_of_nodes(), dg.number_of_edges()
	print "degree_centrality(dg):", nx.degree_centrality(dg)
	print "in_degree_centrality(dg):", nx.in_degree_centrality(dg)
	print "out_degree_centrality(dg):", nx.out_degree_centrality(dg)
	print "number of isolated nodes",'\t\t',nx.isolates(dg)
	print "degree (minimum, average, maximum):", '\t\t', getMinAvgMax(dg.degree())
	
	try:
		print "diameter",'\t\t', nx.diameter(dg)
	except:
		print "error"
	
	try:
		print "radius",'\t\t', nx.radius(dg)
	except:
		print "error"
	
	try:
		print "is_bipartite?",'\t\t', bipartite.is_bipartite(dg)
	except:
		print "error"
	
	try:
		print "average_shortest_path_length",'\t\t', nx.average_shortest_path_length(dg)
	except:
		print "error"
	
	try:
		print "degree_assortativity_coefficient",'\t\t', nx.degree_assortativity_coefficient(dg)
	except:
		print "error"
	
	try:
		print "assortativity.average_degree_connectivity",'\t\t', nx.assortativity.average_degree_connectivity(dg)
	except:
		print "error"
	
	# iter = dg.nodes_iter()
	# for x in range(8):
		# node = iter.next()
		# print "node name and id ", node, twitterIDs[node]
		# print 'successors:', dg.successors(node)
		# print 'predecessors:', dg.predecessors(node)

def getMinAvgMax(myDict):
	values = myDict.values()
	minimum = min(values)
	maximum = max(values)
	average = sum(values)/float(len(myDict))
	return minimum, average, maximum

	
savedPath = os.getcwd()
__main__()
os.chdir(savedPath)