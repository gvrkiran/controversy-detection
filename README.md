# controversy-detection

Code and networks used in the paper "Quantifying Controversy in Social media"

Structure

code/ # contains all the code
	controversy_measures

networks/ # contains all the netwroks
	retweet_networks/ # all retweet networks we created
	follow_networks/ # all follow networks we created

Code for computing polarization scores:

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



All these scripts for computing polarization scores depend on the presence of a "communities_{retweet,follow}_networks" folder. Community detection was done using Metis. Any other community detection can be used to obtain 2 communities.
