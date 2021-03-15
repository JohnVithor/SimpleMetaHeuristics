import random
import numpy as np
import networkx as nx
from Problem import Problem
from LocalSearch import LocalSearch
from GreedSearch import GreedSearch
from VNS import VariableNeighborhoodSearch
from GRASP import GRASP

seed = 0

if __name__== "__main__" :
    Problem.files_path = ''
    problem = Problem('grafo_exemplo', '.graphml')

    problem.nx_graph['1']['2']['weight'] = 4
    problem.nx_graph['1']['3']['weight'] = 5
    problem.nx_graph['1']['7']['weight'] = 4
    problem.nx_graph['2']['3']['weight'] = 5
    problem.nx_graph['2']['4']['weight'] = 6
    problem.nx_graph['3']['4']['weight'] = 11
    problem.nx_graph['3']['5']['weight'] = 8
    problem.nx_graph['3']['6']['weight'] = 7
    problem.nx_graph['3']['7']['weight'] = 10
    problem.nx_graph['4']['5']['weight'] = 3
    problem.nx_graph['5']['6']['weight'] = 1
    problem.nx_graph['6']['7']['weight'] = 3
    problem.distance_matrix = nx.to_numpy_matrix(problem.nx_graph)

    for line in range(problem.size):
        problem.distance_matrix[line] = np.where(problem.distance_matrix[line]==0, np.inf, problem.distance_matrix[line])
        problem.distance_matrix[line, line] = 0

    random_tour = problem.random_solve(seed)
    print('random tour:', random_tour)
    print('random tour cost:', problem.evaluate(random_tour))

    local_search = LocalSearch(problem)
    local_search_tour = local_search.search(random_tour, 1)
    print('local_search tour:', local_search_tour)
    print('local_search tour cost:', problem.evaluate(local_search_tour))

    greed_tour = GreedSearch.search(problem)
    print('greed tour:', greed_tour)
    print('greed tour cost:', problem.evaluate(greed_tour)) 

    vns = VariableNeighborhoodSearch(problem, None, seed)
    vns_tour, step, last_update = vns.run(3, 100, 10)
    print('vns tour cost:', problem.evaluate(vns_tour))
    print('total steps', step)
    print('last update', last_update)

    grasp = GRASP(problem, None, seed)
    grasp_tour, step, last_update = grasp.run(0.1, 2, 100, 50)
    print('grasp tour cost:', problem.evaluate(grasp_tour))
    print('total steps', step)
    print('last update', last_update)