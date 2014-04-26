import readline, glob # for getting filename
import os, statistics, heapq
import openpyxl as xl
import numpy as np
import networkx as nx
import community
from networkx.algorithms import bipartite

def __main__():
	
	filepath = getFilepath()
	print "reading:", filepath, "...",
	workbook = xl.load_workbook(filename = filepath) ## workbook LONG
	print "done!"
	
	twitterIDs = {}
	fullDG = nx.DiGraph() ## creating a directed graph
	
	sheetNames = workbook.get_sheet_names()
	ws = workbook.get_sheet_by_name(sheetNames[0])
	print 'reading id sheet:', ws.title, "...",
	for row in ws.rows[1:]:
		id = row[0].value
		name = row[2].value
		twitterIDs[id] = name
		fullDG.add_node(id)
	print "done!"
	
	for sheetName in sheetNames[1:]:
		ws = workbook.get_sheet_by_name(sheetName)
		print 'reading relation sheet:', ws.title, "...",
		for row in ws.rows[1:]:
			source = row[0].value
			dest = row[1].value
			if source is None or dest is None:
				continue
			edge = row[4].value
			if edge:
				sToD = row[2]
				dToS = row[3]
				if sToD:
					fullDG.add_edge(source, dest)
				if dToS:
					fullDG.add_edge(dest, source)
		print "done!"
	
	connDG = nx.DiGraph(data=fullDG)
	connDG.remove_nodes_from(nx.isolates(connDG))
	
	graphNames = ('Complete', 'Connected')
	graphs = (fullDG, connDG)
	
	for graph, name in zip(graphs, graphNames):
		print "Analysis for",name,"twitter graph:"
		print "Number of nodes/edges: ", graph.number_of_nodes(),'\t', graph.number_of_edges()
		
		numDisplay = min(len(graph.nodes())/5, 5)
		
		statNames = ('degree', 'in degree', 'out degree')
		centralityFuncts = (nx.degree_centrality, nx.in_degree_centrality, nx.out_degree_centrality)
		## for statName, graphFunct in zip(statNames, centralityFuncts):
		for statName, graphFunct in zip(statNames[:1], centralityFuncts[:1]):
			statDict = graphFunct(graph)
			
			ends = ("greatest", dict_nlargest), ("least", dict_nsmallest)
			for endName, endFunct in ends:
				displayDict = endFunct(statDict, numDisplay)
				print numDisplay, endName, statName, "centrality nodes:"
				for key in displayDict:
					print "\t", twitterIDs[key], ":\t", graph.degree(key)
					# print "\t", nx.info(graph, key)
					# print "\t", twitterIDs[key], ":\t", displayDict[key], "\t", 
					
		print "number of isolated nodes",'\t\t',len(nx.isolates(graph))
		print "degree (minimum, average, maximum):", '\t\t', getMinAvgMax(graph.degree())
		
		try:
			print "diameter",'\t\t', nx.diameter(graph)
		except:
			print "error"
		
		try:
			print "radius",'\t\t', nx.radius(graph)
		except:
			print "error"
		
		try:
			print "is_bipartite?",'\t\t', bipartite.is_bipartite(graph)
		except:
			print "error"
		
		try:
			print "average_shortest_path_length",'\t\t', nx.average_shortest_path_length(graph)
		except:
			print "error"
		
		try:
			print "degree_assortativity_coefficient",'\t\t', nx.degree_assortativity_coefficient(graph)
		except:
			print "error"
		
		try:
			print "assortativity.average_degree_connectivity",'\t\t', nx.assortativity.average_degree_connectivity(graph)
		except:
			print "error"
			
		print
		
		# iter = graph.nodes_iter()
		# for x in range(8):
			# node = iter.next()
			# print "node name and id ", node, twitterIDs[node]
			# print 'successors:', graph.successors(node)
			# print 'predecessors:', graph.predecessors(node)

def getFilepath():
	def complete(text, state):
		return (glob.glob(text+'*.xlsx')+[None])[state]
		
	readline.set_completer_delims(' \t\n;')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(complete)
	
	dirFiles = [f for f in os.listdir('.') if os.path.isfile(f)]
	validFiles = [file for file in dirFiles if file[-5:] == '.xlsx']
	
	print "Availible files for analysis:"
	for file in validFiles:
		print '\t'+file
		
	while True:
		input = raw_input('Enter which excel file for twitter analysis: ').strip()
		if input in validFiles:
			return input
		print "Please enter a valid file"
		
def getMinAvgMax(myDict):
	values = myDict.values()
	minimum = min(values)
	maximum = max(values)
	average = sum(values)/float(len(myDict))
	return minimum, average, maximum
	
def dict_nsmallest(dict, n):
	returnDict = {}
	for key in heapq.nlargest(n ,dict, key = lambda k: -dict[k]):
		returnDict[key] = dict[key]
	return returnDict
	
def dict_nlargest(dict, n):
	returnDict = {}
	for key in heapq.nlargest(n ,dict, key = lambda k: dict[k]):
		returnDict[key] = dict[key]
	return returnDict
	# return heapq.nlargest(n ,dict, key = lambda k: dict[k])
	
__main__()