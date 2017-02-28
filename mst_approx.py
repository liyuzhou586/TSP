# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 14:46:56 2016

@author: dengzheng
"""

#MST-APPROX
import random
import time 
import networkx as nx 
import math
import heapq as hp
import sys
"""
Run_MSTapprox(filename,cutofftime,randomseed)
is the main run function to compute the results by using other function in MST approximation
@input: finename, cutofftime, randomsedd 
@output: .sol file and .trace file
@
MSTapprox(G)
is the function to compute MST approximation by taking a graph as input
@input: graph
@output: total_tour, total_cost, total_time,path
@
Distance(x1,y1,x2,y2)
is the function to compute distance between point1(x1,y1) and point2(x2,y2) in 
Euclidean distance accroding to TSPLIB
@
Readfile(filename)
is the function to take filename as input to store the data of every point
@
AdjacencyMatrix(pointrecord)
is the function to take data of points and generate the Adjacency Matrix sotre as G(graph)
@
computeMST(G)
is the function to compute MST of a given graph--G
@
Eulerian_graph(MST)
is the function to double every edge in MST
@
depth_first_search(edge_list)
is the function to compute depth first search of a input edge list
@
compute_path(path_nodes, G)
is the function to compute the final path
@
compute_tour(path)
is the function to compute the final tour of each node by taking the final path
@
compute_cost(path)
is the function to compute the final cost of this algorithm by taking the final path
@
main()
is the main function to execute this program in terminal
"""
def Run_MSTapprox(filename,cutofftime,randomseed):
    point_data = Readfile(filename)
    G = AdjacencyMatrix(point_data)

    trace = open('../output/'+filename.split('.')[0] + '_MSTApprox_' + str(cutofftime) + '_' + str(randomseed) + '.trace','w')
    solution = open('../output/'+filename.split('.')[0] + '_MSTApprox_' + str(cutofftime) + '_' + str(randomseed) + '.sol','w')
    final_cost = 0
    random.seed(randomseed)
    for i in range(cutofftime):
        total_tour, total_cost, total_time,path = MSTapprox(G)
#        print(total_tour)
        if i == 0:
            trace.write(str(total_time) + ' ' + str(total_cost) + '\n')
            final_cost = total_cost
            solution.write(str(total_cost) + '\n')
            for j in range(0,len(total_tour),2):
            #step is 2
                for item in path:
                    if total_tour[j] == item[0]:
                        solution.write(str(total_tour[j]) + ' ' + str(item[1]) + ' ' + str(item[2]) + '\n')
            solution.close()    
            

        else:
            if total_cost < final_cost:
                trace.write(str(total_time) + ' ' + str(total_cost) + '\n')
                final_cost = total_cost
                solution = open('../output/'+filename.split('.')[0] + '_MSTApprox_' + str(cutofftime) + '_' + str(randomseed) + '.sol','w')
                solution.write(str(total_cost) + '\n')
                for j in range(0,len(total_tour),2):
                    for item in path:
                        if total_tour[j] == item[0]:
                            solution.write(str(total_tour[j]) + ' ' + str(item[1]) + ' ' + str(item[2]) + '\n')
                solution.close()
    trace.close()

def MSTapprox(G):
    
    start_time = time.time()
    MST = MST=computeMST(G)
    double_MST = Eulerian_graph(MST)
    
    dfs_path = depth_first_search(double_MST)
    
    path = compute_path(dfs_path, G)
    
    total_tour = compute_tour(path)
    total_time = time.time() - start_time
    total_cost =compute_cost(path)
    
    return total_tour, total_cost, total_time,path
    
    
    


def Distance(x1,y1,x2,y2):
    #Compute the 2-D (Euclidean) distance between two points.
    x_d = (x1 - x2)
    y_d = (y1 - y2)
    return int(math.sqrt(x_d**2 + y_d**2) + 0.5)
    
def Readfile(filename):
    file = open('./DATA/'+filename,'r')
    line = file.readline()
    while line.find("NODE_COORD_SECTION") == -1:
        line = file.readline()
    point_data = {}
    while 1:
        line = file.readline()
        if line.find("EOF") != -1: 
            break
        (i,x,y) = line.split()
        i = int(i)
        x = float(x)
        y = float(y)
        
        point_data[i] =(x,y)
    return point_data

def AdjacencyMatrix(pointrecord):
    #compute and store distance between every pairs points in a matrix
    #pointrecord is a list of point (x1,y1),(x2,y2)....
    adjacencyM = {}
    for i in pointrecord:
        adjacencyM[i] = {}
        for j in pointrecord:
            x1,y1 = pointrecord[i]
            x2,y2 = pointrecord[j]
            dist = Distance(x1,y1,x2,y2)
            
            adjacencyM[i][j] = dist
    return adjacencyM



 
    
    
def computeMST(G):
    MST=[]
    heap_result=[]
    
    
#    MST_weight=0
    passed={}
    for point in G:
        passed[point] = 1
        for j in range(len(G[point])):
            hp.heappush(heap_result,(G[point][j+1],point,j+1))
            
        while len(heap_result) != 0:
            current = hp.heappop(heap_result)

            next_one = current[2]
      
            if passed.get(next_one) == None:
                passed[next_one] = 1
                MST.append(current)
#                MST_weight += int(current[0])
                for i in range(len(G[next_one])):
                    hp.heappush(heap_result,(G[next_one][i+1],next_one,i+1))
        break

    return MST
 
def Eulerian_graph(MST):
    """double every edge in MST to obtain an eulerian graph"""
    
    reverse_edges = [(x[2],x[1],x[0]) for x in MST]
    MST = [(x[1],x[2],x[0]) for x in MST]
    double_edge_list = reverse_edges + MST
    return double_edge_list

def depth_first_search(edge_list):
    """This function does a depth first search of a graph
       edge list is the double MST edge_list
    """
    
    G_temp = nx.Graph()
    G_temp.add_weighted_edges_from(edge_list)
    edge_index = random.randint(0, len(edge_list) - 1)
    dfs_path = list(nx.dfs_preorder_nodes(G_temp,edge_list[edge_index][0]))
                                               
    return dfs_path

def compute_path(path_nodes, G):
    '''
    This function get get the weights for the node path.
    path_nodes is the depth first search path.
    edge_list is double MST edge_list
    '''
#    print(path_nodes)
    path = []
    n_nodes = len(path_nodes)
    for node in G:
        for i in range(n_nodes):
            node_i = path_nodes[i]
            node_next = path_nodes[(i + 1) % n_nodes]
            if node == node_i:
                path.append((node_i, node_next, G[node_i][node_next])) 
                """edge[2] is weight(distance)"""
            
    return path
    
def compute_node(path):
    copy_path = path[:]
#    copy_path = []
#    for i in path:
#        if i not in copy_path:
#            copy_path.append(i)
#    print(copy_path)
    
    first_edge = copy_path.pop()
    node_list = [first_edge[0], first_edge[1]]
    
    while node_list.count(node_list[-1]) < 2:
        for edge in copy_path:
            if edge[0] == node_list[-1]:
                node_list.append(edge[1])
                copy_path.remove(edge)
                
            elif edge[1] == node_list[-1]:
                node_list.append(edge[0])
                copy_path.remove(edge)
                
    return node_list

def compute_tour(path):
    '''
    Get tour of graph starting with node v1, v2, v2, ..., vn, v1.
    '''
    node_list = compute_node(path)
    tour = [node_list[0]]
    for node in node_list[1:]:
        tour.append(node)
        tour.append(node)
    return tour[:-1]

def compute_cost(path):
    '''
    This function retuns the total cost of a solution path.
    '''
    total_cost = 0
    for edge in path:
        total_cost += edge[2]
    return total_cost

def main():
    num_args = len(sys.argv)
    if num_args < 3:
        print("error:not enough input argument")
        exit(1)
    filename = sys.argv[1]
    cutofftime = sys.argv[2]
    randomseed = sys.argv[3]
    Run_MSTapprox(filename,int(cutofftime),int(randomseed))

if __name__ == '__main__':
    main() 
    

#point_data = Readfile('Atlanta.tsp')
#G=AdjacencyMatrix(point_data)
##print(G)
#MST=computeMST(G)
#
#double_g=Eulerian_graph(MST)
#
##print(double_g)
#
#path_sequence=depth_first_search(double_g)
##print(path_sequence)
##print(MST)  
#path=edge_list_path(path_sequence,G)
##print(path)
#
#node_list=compute_node_list(path)
##print(node_list)
#tour= compute_tour(path)
#cost=compute_cost(path)
#print(cost)
#print(tour)
#Run_MSTapprox('Toronto.tsp',600,3)


    
    
    