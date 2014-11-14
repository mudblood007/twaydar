# TwaydarGUN: Twitter Graph-based Update Numeration, v.0.1.4
# Latest Revision: November 10, 2014
# VMB Silenzio, URochester

import networkx as nx
import matplotlib.pyplot as plt

#   GRAPH DEFINITION
#   Initiates a random graph using the Holme and Kim algorithm for growing
#   graphs with power law degree distribution and approximate average clustering
#   See P Holme and BJ Kim, "Growing scale-free networks with tunable
#   clustering", Phys Rev E, 65, 026107, 2002


#   Set parameters for graph generation

#   Number of nodes n | int
# n = 10000
n = input('How many nodes in the network?: ')

#   m = random edges for each node  | int
# m = 3
m = input('How many random edges to add for each node?: ')

#   p = probablility of adding a triangle after adding random edge | float
# p = 0.1
p = input('What is the probability (from 0 to 1) of adding a triangle when adding a randome edge?: ')


G = nx.powerlaw_cluster_graph(n, m, p, seed=None)


#   Set sexual orientation scores (SO_score) to Nil
i = n-1
while i >= 0:
    G.add_node(i, SO_score=0.0)
    i -= 1

#   Set the number of definitive seeds
lgb_seeds = input('How many nodes should be labeled as LGB?: ')
het_seeds = input('How many nodes should be labeled as heterosexual?: ')
# lgb_prop = input('What proportion of LGB node neighbors are also LGB? (The literature suggests p = 0.4): ')
lgb_prop = 0.4
lgb_weight = (1 - lgb_prop)
#   TODO: Clarify why I decided the weight is the inverse probability

# het_prop = input('What proportion of heterosexual node neighbors are also heterosexual? (The literature suggests p = 0.9: ')
het_prop = 0.9
het_weight = (1 - het_prop)
#   TODO: Clarify why I decided the weight is the inverse probability

#   N.B. The logic here for these weights is that the 'implication' of having
#   a straight or non-straight friend is not equivalent


#   Randomly assign sexual orientation seeds for the toy network
import random

i = lgb_seeds
while i > 0:
    lgb_node = random.randint(0,n-1)
    if G.node[lgb_node]['SO_score'] == 0.0:
        G.add_node(lgb_node, SO_score=1.0)
        i -= 1
    else:
        i -= 1
    continue

i = het_seeds
while i > 0:
    het_node = random.randint(0,n-1)
    if G.node[het_node]['SO_score'] == 1.0:
        i -= 1
        continue
    else:
        G.add_node(het_node, SO_score=-1.0)
        i -= 1

#   Sanity Check: Print out the initial SO_score values
#i = n-1
#while i > 0:
#    print(i, G.node[i])
#    i -= 1


#   GLU[E] GRAPH-BASED LABEL UPDATE [ENGINE]
#   
#   N.B. Ultimately, GLU[E] would be spun off as a separate module to operate
#   across applications of this approach to other use cases

#   Cycle through each node of the network and update SO_score for these
#   N.B. Following Pennacchioti & Popescu (KDD'11), 'score' refers to the
#   classification confidence value, ranging from -1 to +1
#   [[TODO]]
i = n-1

while i >= 0:
    #   Set initial score
    score = G.node[i]['SO_score']

    #   Define a vector of neighboring nodes
    a = nx.neighbors(G,i)
    j = len(a)-1

    sum = 0

    #   Work through each element of the vector of neighboring nodes
    while j >= 0:
        # Skipping known "solidly gay" nodes
        if G.node[a[j]]['SO_score'] == 1:
            j -= 1
            continue

        # Skipping known "solidly straight" nodes
        elif G.node[a[j]]['SO_score'] == -1:
            j -= 1
            continue

        # Skipping "unknown" nodes
        elif G.node[a[j]]['SO_score'] == 0.0:
            # weight = 0
            # sum = sum + (weight * G.node[a[j]]['SO_score'])
            j -= 1
            continue

        # Effect of "gay-leaning" neighbors
        elif G.node[a[j]]['SO_score'] >= 0.0:
            weight = (1-lgb_prop)
            sum = sum + (weight * G.node[a[j]]['SO_score'])
            j -= 1
            continue

        # Effect of "straight-leaning" neighbors
        elif G.node[a[j]]['SO_score'] <= 0.0:
            weight = (1-het_prop)
            sum = sum + (weight * G.node[a[j]]['SO_score'])
            j -= 1
            continue
 #       else: break



    score = score * (sum / len(a))
#    print("Score ", i, " = ", score, sum/len(a))
#    print(len(a))
    i -= 1

nx.draw_spectral(G)
plt.show()

#   Sanity Check 2: Print out the updated SO_score values
#i = n-1
#while i > 0:
#    print(G.node[i])
#    i -= 1
