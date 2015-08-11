# script to compute the score function, based on distances between points in the same cluster and across clusters obtained using the force directed layout

# first run metis (or other community detection algos) to obtain the partitions

import sys,math;
import networkx as nx;
import numpy as np;

filename = sys.argv[1];
file2 = sys.argv[2];

G = nx.read_weighted_edgelist(filename,delimiter=",");

def getDistance(pointa,pointb):
	x1 = pointa[0];
	y1 = pointa[1];
	x2 = pointb[0];
	y2 = pointb[1];
	return math.sqrt((x1-x2)**2 + (y1-y2)**2);

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

#f3 = open("force_directed/" + file2 + "_positions.txt");
f3 = open("force_directed/follower_network/" + file2 + "_positions.txt");
#f3 = open("LinLogLayout/" + file2 + "_positions.txt");
lines3 = f3.readlines();

dict_positions = {};
for i in range(len(lines3)):
	line1 = lines3[i].strip();
	line1_split = line1.split("\t");
	node = line1_split[0];
	[x,y] = [float(line1_split[1].split(",")[0]),float(line1_split[1].split(",")[1])];
	dict_positions[node] = [x,y];

left_list = dict_left.keys();
total_lib_lib = 0.0;
count_lib_lib = 0.0;
avg_lib_lib = 0.0; # average liberal to liberal distance

for i in range(len(left_list)):
	user1 = left_list[i];
	for j in range(i+1,len(left_list)):
		user2 = left_list[j];
		dist = getDistance(dict_positions[user1],dict_positions[user2]);
#		print user1, user2, dist;
		total_lib_lib += dist;
		count_lib_lib += 1.0;
avg_lib_lib = total_lib_lib/count_lib_lib;

right_list = dict_right.keys();
total_cons_cons = 0.0;
count_cons_cons = 0.0;
avg_cons_cons = 0.0; # average conservative to conservative distance

for i in range(len(right_list)):
	user1 = right_list[i];
	for j in range(i+1,len(right_list)):
		user2 = right_list[j];
		dist = getDistance(dict_positions[user1],dict_positions[user2]);
#		print user1, user2, dist;
		total_cons_cons += dist;
		count_cons_cons += 1.0;
avg_cons_cons = total_cons_cons/count_cons_cons;

total_both = 0.0;
count_both = 0.0;
avg_both = 0.0;

for i in range(len(left_list)):
	user1 = left_list[i];
	for j in range(len(right_list)):
		user2 = right_list[j];
		dist = getDistance(dict_positions[user1],dict_positions[user2]);
#		print user1, user2, dist;
		total_both += dist;
		count_both += 1.0;
avg_both = total_both/count_both;

print "********************" + file2 + "*********************";
print avg_lib_lib, avg_cons_cons, avg_both;
print "Score:", 1 - ((avg_lib_lib + avg_cons_cons)/(2*avg_both)), "\n";
