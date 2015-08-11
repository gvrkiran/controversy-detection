# script to compute the polarization score proposed in http://homepages.dcc.ufmg.br/~pcalais/papers/icwsm13-pcalais.pdf
# ICWSM 2013

# first run metis to compute the cut.

import sys;
import networkx as nx;
import numpy as np;

filename = sys.argv[1];
file2 = sys.argv[2];

G = nx.read_weighted_edgelist(filename,delimiter=",");

f1 = open("../communities_retweet_networks/community1_" + file2 + ".txt");
#f1 = open("../communities_follow_networks/community1_" + file2 + ".txt");
lines1 = f1.readlines();
dict_left = {};

for line in lines1:
	line = line.strip();
	dict_left[line] = 1;

f2 = open("../communities_retweet_networks/community2_" + file2 + ".txt");
#f2 = open("../communities_follow_networks/community2_" + file2 + ".txt");
lines2 = f2.readlines();
dict_right = {};

for line in lines2:
	line = line.strip();
	dict_right[line] = 1;

cut_nodes1 = {};
cut_nodes = {};

for i in range(len(lines1)):
	name1 = lines1[i].strip();
	for j in range(len(lines2)):
		name2 = lines2[j].strip();
		if(G.has_edge(name1,name2)):
			cut_nodes1[name1] = 1;
			cut_nodes1[name2] = 1;

dict_across = {}; # num. edges across the cut
dict_internal = {}; # num. edges internal to the cut

def satisfyCondition2(node1): # A node v \in G_i has at least one edge connecting to a member of G_i which is not connected to G_j.
	neighbors = G.neighbors(node1);
	for n in neighbors:
		if(dict_left.has_key(node1) and dict_right.has_key(n)): # only consider neighbors belonging to G_i
			continue;
		if(dict_right.has_key(node1) and dict_left.has_key(n)): # only consider neighbors belonging to G_i
			continue;
		if(not cut_nodes1.has_key(n)):
			return True;
	return False;

# remove nodes from the cut that dont satisfy condition 2 - check for condition2 in the paper http://homepages.dcc.ufmg.br/~pcalais/papers/icwsm13-pcalais.pdf page 5,
for keys in cut_nodes1.keys():
	if(satisfyCondition2(keys)):
		cut_nodes[keys] = 1;

for edge in G.edges():
#	print edge;
	node1 = edge[0];
	node2 = edge[1];
	if(not cut_nodes.has_key(node1) and (not cut_nodes.has_key(node2))): # only consider edges involved in the cut
		continue;
	if(cut_nodes.has_key(node1) and cut_nodes.has_key(node2)): # if both nodes are on the cut and both are on the same side, ignore
		if(dict_left.has_key(node1) and dict_left.has_key(node2)):
			continue;
		if(dict_right.has_key(node1) and dict_right.has_key(node2)):
			continue;
	if(cut_nodes.has_key(node1)):
		if(dict_left.has_key(node1)):
			if(dict_left.has_key(node2) and not cut_nodes1.has_key(node2)):
				if(dict_internal.has_key(node1)):
					dict_internal[node1] += 1;
				else:
					dict_internal[node1] = 1;
			elif(dict_right.has_key(node2) and cut_nodes.has_key(node2)):
				if(dict_across.has_key(node1)):
					dict_across[node1] += 1;
				else:
					dict_across[node1] = 1;
		elif(dict_right.has_key(node1)):
			if(dict_left.has_key(node2) and cut_nodes.has_key(node2)):
				if(dict_across.has_key(node1)):
					dict_across[node1] += 1;
				else:
					dict_across[node1] = 1;
			elif(dict_right.has_key(node2) and not cut_nodes1.has_key(node2)):
				if(dict_internal.has_key(node1)):
					dict_internal[node1] += 1;
				else:
					dict_internal[node1] = 1;
	if(cut_nodes.has_key(node2)):
		if(dict_left.has_key(node2)):
			if(dict_left.has_key(node1) and not cut_nodes1.has_key(node1)):
				if(dict_internal.has_key(node2)):
					dict_internal[node2] += 1;
				else:
					dict_internal[node2] = 1;
			elif(dict_right.has_key(node1) and cut_nodes.has_key(node1)):
				if(dict_across.has_key(node2)):
					dict_across[node2] += 1;
				else:
					dict_across[node2] = 1;
		elif(dict_right.has_key(node2)):
			if(dict_left.has_key(node1) and cut_nodes.has_key(node1)):
				if(dict_across.has_key(node2)):
					dict_across[node2] += 1;
				else:
					dict_across[node2] = 1;
			elif(dict_right.has_key(node1) and not cut_nodes1.has_key(node1)):
				if(dict_internal.has_key(node2)):
					dict_internal[node2] += 1;
				else:
					dict_internal[node2] = 1;

#print dict_internal;
#print dict_across;

polarization_score = 0.0;
lis1 = [];
for keys in cut_nodes.keys():
	if(not dict_internal.has_key(keys) or (not dict_across.has_key(keys))): # for singleton nodes from the cut
		continue;
	if(dict_across[keys]==0 and dict_internal[keys]==0): # theres some problem
		print "wtf";
#	print dict_internal[keys],dict_across[keys],(dict_internal[keys]*1.0/(dict_internal[keys] + dict_across[keys]) - 0.5),G.degree(keys);
	polarization_score += (dict_internal[keys]*1.0/(dict_internal[keys] + dict_across[keys]) - 0.5);
#	if(polarization_score==0.0):
#		continue;
#	lis1.append(polarization_score);

polarization_score = polarization_score/len(cut_nodes.keys());
print "********************" + file2 + "*********************";
print polarization_score, "\n";
#print np.mean(np.asarray(lis1)), np.median(np.asarray(lis1));
