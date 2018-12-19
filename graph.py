from collections import deque
from heapq import heappush, heappop
import matplotlib.pyplot as plt
from math import cos, sin, pi, log


class Graph:
    def __init__(self, oriented=False):
        self.nodes = []
        self.edges = {}
        self.distances = {}
        self.oriented = oriented

    def add_node(self, value):
        self.nodes.append(value)
        self.edges[value] = []

    def add_edge(self, from_node, to_node, distance=1):
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance
        if not self.oriented :
            self.edges[to_node].append(from_node)
            self.distances[(to_node, from_node)] = distance

    
    def del_edge(self, from_node, to_node):
        del self.edges[from_node][self.edges[from_node].index(to_node)]
        del self.distances[(from_node, to_node)]
        if not self.oriented :
            del self.edges[to_node][self.edges[to_node].index(from_node)]
            del self.distances[(to_node, from_node)]


    def dijsktra(self, initial, final=None):
        # find shortest path starting from initial node to final node
        # if there is no final node, returns shortest path to every reachable node
        colors = {}
        distances = {}
        prec = {}
        for n in self.nodes :
            colors[n] = 0
            distances[n] = float('inf')

        heap = [(0,initial)]
        distances[initial] = 0
        prec[initial] = None

        while heap : 
            a, node = heappop(heap)
            if node == final :
                path = [node]
                while prec[node] :
                    node = prec[node]
                    path.append(node)
                path.reverse()
                return distances[final], path
            if colors[node] == 0 : 
                colors[node] = 1
                for neighbour in self.edges[node] :
                    d = distances[node]+self.distances[node, neighbour]
                    if d < distances[neighbour]  :
                        prec[neighbour] = node
                        heappush(heap, (d,neighbour))
                        distances[neighbour] = d
        if final==None :
            return distances, prec
        return float('inf'), []


    def floyd_warshall(self) :
    # compute minimal distance from each node to each other node
        for i in self.nodes :
            for j in self.nodes : 
                try : 
                    self.distances[i,j]
                except :
                    self.distances[i,j] = float('inf')

        for k in self.nodes :
            for i in self.nodes :
                for j in self.nodes : 
                    if self.distances[i,j]>self.distances[i,k]+self.distances[k,j] :
                        self.distances[i,j]=self.distances[i,k]+self.distances[k,j]

    def prim(self) :
    # return minimum spanning tree 
        g = Graph() 
        colors = {}
        for node in self.nodes :
            g.add_node(node)
        heap = [(0,None,node)]

        for n in self.nodes :
            colors[n] = 0

        total = 0
        while heap :
            d, prec, node = heappop(heap)
            if not colors[node] :
                colors[node]=1
                if prec!=None :
                    g.add_edge(prec,node,d)
                    g.add_edge(node,prec,d)
                    total+=d
                for neighbour in self.edges[node] :
                    heappush(heap, (self.distances[node, neighbour], node, neighbour))
        return total, g

    def __repr__(self) :
        n = len(self.nodes)
        pos = {}
        for i,node in enumerate(self.nodes) :
            pos[node] = 2*pi*i/n
        for u in pos.values() :
            plt.plot([cos(u)], [sin(u)], 'ro')

        if self.oriented :
            hw = 0.02
        else :
            hw = 0
        for node in self.nodes :
            for neighbour in self.edges[node] :
                x1 = cos(pos[node])
                y1 = sin(pos[node])
                x2 = cos(pos[neighbour])-x1
                y2 = sin(pos[neighbour])-y1
                plt.arrow(x1, y1, 2/3*x2, 2/3*y2, 'b',length_includes_head=True, head_width=hw)
                plt.arrow(x1+2/3*x2, y1+2/3*y2, 1/3*x2, 1/3*y2, 'b',length_includes_head=True, head_width=0)

        plt.show()
        return 'see plot'


if __name__ == '__main__':
    g = Graph(oriented=True)
    N = 10
    for i in range(N) :
        g.add_node(i)
    for i in range(N) :
        g.add_edge(i,(i+1)%N)
        g.add_edge(i,(i-3)%N)

    distance, path = g.dijsktra(0, 5)
    print("shortest path from 0 to 5:", path, "(length:", distance,")")
    print(g)
    g2 = g.prim()
    print(g2)