# controversy-detection

Code and networks used in the paper "Quantifying Controversy in Social media"
Author: Kiran Garimella (kiran.garimella@aalto.fi)

Structure

code/ # contains all the code
	controversy_measures

	a. Code for computing polarization scores:

	1. edge_betweenness/ 
		computePolarizationScoreEdgebetweenness.py
	2. randomwalk/
		computePolarizationScoreRandomwalk.py
	3. force_directed/
		computePolarizationScoreForceDirected.py
		forceatlas.py -- Code for computing the Force directed embeddings
	4. GMCK/
		computePolarizationScoreICWSM.py
	5. MBLB/
		computePolarizationScoreVenezuela.py

	All these scripts for computing polarization scores depend on the presence of a "communities_{retweet,follow}_networks" folder. See below.

	b. Additional folders:
	
	1. community_detection_retweet_networks/ -- contains communities obtained from the retweet networks in ../networks/retweet_networks
	2. community_detection_follow_networks/ -- contains communities obtained from the retweet networks in ../networks/follow_networks
	3. edge_betweenness/ -- edge betweenness of the networks, used by the edge_betweenness polarization measure.

	Community detection was done using Metis. Any other community detection can be used to obtain 2 communities.

------------------------------------

networks/ # contains all the netwroks
	retweet_networks/ # all retweet networks we created (only the largest connected component)
	follow_networks/ # all follow networks we created

