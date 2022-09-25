from sys import stderr

import networkx as nx
import matplotlib.pyplot as plt

class Plot:
  def __init__(self):
    self.graph = None
    self.num_vertices = None
    self.num_edges = None
    self.weighted = None

  def import_instance(self, full_path:str):
    lines = open(full_path, 'r').readlines()
    self.num_vertices = lines[0].split()[0]
    self.num_edges = lines[0].split()[1]
    self.weighted = lines[0].split()[2]

    if self.weighted:
      weights = lines[1]
      edges = lines[2].replace(', ',',').replace(')(',') (')
    else:
      edges = lines[2].replace(', ',',').replace(')(',') (')

    edges = [eval (t) for t in edges]
    self.graph = nx.Graph()
    self.graph.add_edges_from(edges)
    self.graph.add_nodes_from([int(n) for n in range(self.num_vertices)])

    i = 0
    for v in sorted(self.graph.nodes()):
      if self.weighted:
        self.graph.add_node(v, weight=weights[i])
      else:
        self.graph.add_node(v, weight=1)
      i = i+1 
      

  def plot_graph(self):
    pos = nx.spring_layout(self.graph, seed=3113794652)
    #nx.draw_networkx(graph,pos,node_size=500,width=2,with_labels=True)
    if not self.weighted:
      nx.draw_networkx(self.graph,pos,node_color='#00b4d9',node_size=500,width=2,with_labels=True)
    else:
      labels = nx.get_node_attributes(self.graph, 'weight')
      nx.draw_networkx(self.graph,pos,node_color='#00b4d9',node_size=500,width=2,with_labels=True)
      for v in self.graph.nodes():
        x,y=pos[v]
        plt.text(x,y+0.15,s=labels[v], bbox=dict(facecolor='white', alpha=0.5),horizontalalignment='center')
    ax = plt.gca()
    ax.set_title('Graph')
    ax.margins(0.20)
    plt.axis("off")

    plt.show()

  def plot_mvc(self, vertices:str, edges:list, approx=0):
    pos = nx.spring_layout(self.graph, seed=3113794652)
    vertices = [int(i) for i in vertices.split()]
    v_color_map = []
    e_color_map = []

    for node in self.graph.nodes():
      if node in vertices:
        v_color_map.append('red')
      else:
        v_color_map.append('#00b4d9')

    for e in graph.edges():
      if e in edges:
        e_color_map.append('black')
      else:
        e_color_map.append('lightgrey')

    if not self.weighted:
      nx.draw_networkx(self.graph,pos,node_color=v_color_map,node_size=500,edge_color=e_color_map,width=2,with_labels=True)
    else:
      labels = nx.get_node_attributes(self.graph, 'weight') 
      nx.draw_networkx(self.graph,pos,node_color=v_color_map,node_size=500,edge_color=e_color_map,width=2,with_labels=True)
      for v in self.graph.nodes():
        x,y=pos[v]
        plt.text(x,y+0.15,s=labels[v], bbox=dict(facecolor='white', alpha=0.5),horizontalalignment='center')

    ax = plt.gca()

    if not self.weighted:
      ax.set_title('Minimum Vertex Cover (red nodes)')
    else:
      if approx == 0:
        ax.set_title('Minimum Weight Vertex Cover (red nodes)')
      else:
        ax.set_title('2-Approximated Minimum Weight Vertex Cover (red nodes)')

    ax.margins(0.20)
    plt.axis("off")

    plt.show()

  def plot_2apx_vc(self, vertices:str, edges:list):
    pos = nx.spring_layout(self.graph, seed=3113794652)
    vertices = [int(i) for i in vertices.split()]
    v_color_map = []
    e_color_map = []
    for node in self.graph.nodes():
      if node in vertices:
        v_color_map.append('red')
      else:
        v_color_map.append('#00b4d9')
    #edges = edges.replace(', ', ',')
    #edges = [eval(t) for t in edges.split()]
    edges = [tuple(sorted(t)) for t in edges]
    for e in self.graph.edges():
      if e in edges:
        #e_color_map.append('red')
        e_color_map.append('black')
      else:
        e_color_map.append('lightgrey')
    nx.draw_networkx(self.graph,pos,node_color=v_color_map,node_size=500,edge_color=e_color_map,width=2,with_labels=True)            
    ax = plt.gca()
    ax.set_title('2-approximated Vertex Cover')
    ax.margins(0.20)
    plt.axis("off")

    plt.show()

  def plot_indset(self, vertices:str, edges:list, weighted=0):
    pos = nx.spring_layout(self.graph, seed=3113794652)
    vertices = [int(i) for i in vertices.split()]
    v_color_map = []
    e_color_map = []

    for node in self.graph.nodes():
      if node in vertices:
        v_color_map.append('red')
      else:
        v_color_map.append('#00b4d9')

    for e in self.graph.edges():
      if e in edges:
        e_color_map.append('black')
      else:
        e_color_map.append('lightgrey')

    if not self.weighted:
      nx.draw_networkx(self.graph,pos,node_color=v_color_map,node_size=500,edge_color=e_color_map,width=2,with_labels=True)
    else:
      labels = nx.get_node_attributes(self.graph, 'weight')
      nx.draw_networkx(self.graph,pos,node_color=v_color_map,node_size=500,edge_color=e_color_map,width=2,with_labels=True)
      for v in self.graph.nodes():
        x,y=pos[v]
        plt.text(x,y+0.15,s=labels[v], bbox=dict(facecolor='white', alpha=0.5),horizontalalignment='center')

    ax = plt.gca()

    if not self.weighted:
      ax.set_title('Maximum Independent Set (red nodes)')
    else:
      ax.set_title('Maximum Weight Independent Set (red nodes)')

    ax.margins(0.20)
    plt.axis("off")

    plt.show()

def main():
  pass

if __name__ == '__main__':
    main()


