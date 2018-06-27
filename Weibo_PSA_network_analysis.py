#tutorial: https://networkx.github.io/documentation/networkx-1.9/tutorial/tutorial.html

import json
import networkx as nx
import matplotlib.pyplot as plt


with open('weibo_PSA.json', encoding="utf-8") as file:
    data = json.load(file)

node_lst = list()
edge_lst = list()
for info in data:
    #if int(info['reposts_count'])!= 0:
    post = info['post_id'] #post refers to the weibo post that reposts another post
    repost = info['retweeted_id'] #repost refers to the weibo post that is reposted
    #generate a graph for edges
    g_edges = nx.Graph()
    g_edges.add_edge(repost, post)
    for (a,b) in g_edges.edges:
        edge_lst.append((a,b))
    #generate a graph for nodes
    g_nodes = nx.Graph()
    g_nodes.add_node(repost)
    g_nodes.add_node(post)
    for node in g_nodes.nodes:
        node_lst.append(node)


print('edge list:',edge_lst) #equals to g.edges

#calculate the between centrality of nodes in the network
g = nx.Graph()
dg = nx.DiGraph(g)

g.add_edges_from(edge_lst)
dg.add_edges_from(edge_lst)
dg.add_nodes_from(node_lst)
#print('node list:',dg.nodes)
#print('edge list:',dg.edges)

#nx.write_gexf(dg,'weibo_PSA_network.gexf')


#print(nx.degree_centrality(dg))
print(nx.degree_centrality(g))
#print(nx.betweenness_centrality(g,normalized=True))


# %matplotlib inline
#
# plt.figure(figsize=(20,20))
#
#
# BLUE='#99CCFF'
#
# nx.draw_networkx(dg,pos = nx.spring_layout(dg,scale=2),node_color='lightblue',
#     linewidths=0.0000001, font_size=0.5, font_weight='bold', with_labels=True, dpi=1000)
#plt.savefig("weibo_PSA.png")