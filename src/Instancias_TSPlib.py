import random
import numpy as np
import networkx as nx
from Solve import Solve
from Problem import Problem
from LocalSearch import LocalSearch
from GreedSearch import GreedSearch
from VNS import VariableNeighborhoodSearch
from GRASP import GRASP

import pandas as pd
import time
import multiprocessing
import sys

seed = 0
max_exec_time_per_run_in_minutes = 1
max_exec_time_per_run_in_seconds = 60.0 * max_exec_time_per_run_in_minutes
n_cores = 1
result_file_name = "results.csv"


  ## Define some functions to run VNS and GRASP


def simple_vns_run(args):
  global seed
  problem, k, max_it, no_upt, max_time, greed_solve = args
  print('VNS Started: Problem: ', problem.instance_name)  
  vns = VariableNeighborhoodSearch(problem, None, seed)
  start_time = time.time()
  vns_tour, step, last_update = vns.run(k, max_it, no_upt, max_time, greed_solve)
  end_time = time.time()
  vns_cost = problem.evaluate(vns_tour)
  # print('    Time to run vns: ', end_time-start_time, 'seconds')
  # print('    vns tour cost:', vns_cost)
  # print('    total steps', step)
  # print('    last update', last_update)
  print('VNS Done: Problem: ', problem.instance_name)  
  return vns_cost, end_time-start_time, vns_tour, step, last_update

def simple_grasp_run(args):
  global seed
  problem, alpha, k, max_it, no_upt, start_incr, max_time = args
  print('GRASP Started: Problem: ', problem.instance_name)  
  grasp = GRASP(problem, None, seed)
  start_time = time.time()
  grasp_tour, step, last_update = grasp.run(alpha, k, max_it, no_upt, start_incr, max_time)
  end_time = time.time()
  grasp_cost = problem.evaluate(grasp_tour)
  # print('    Time to run grasp: ', end_time-start_time, 'seconds')
  # print('    grasp tour cost:', grasp_cost)
  # print('    total steps', step)
  # print('    last update', last_update)
  print('GRASP Done: Problem: ', problem.instance_name)  
  return grasp_cost, end_time-start_time, grasp_tour, step, last_update


  ### Start the main problem ###


if __name__== '__main__' :

  if len(sys.argv) != 5:
    print("É necessario informar:")
    print("A seed para gerar os números aleatorios")
    print("O tempo máximo de execução de cada algoritmo em uma instancia, em minutos")
    print("O número máximo de execuções que podem rodar em paralelo")
    print("O nome do arquivo de saida com os resultados dos algoritmos")
    sys.exit(1)

  ### Set the seed to the random number generator ###
  ### Set the max time per run of algorithm ###
  ### Get the number of available cores ###

  seed = int(sys.argv[1])
  max_exec_time_per_run_in_minutes = float(sys.argv[2])
  max_exec_time_per_run_in_seconds = 60.0 * max_exec_time_per_run_in_minutes
  n_cores = int(sys.argv[3])
  result_file_name = sys.argv[4]

  ### Load instance list ###


  table_problems = pd.read_csv('TSP - PCV Instancias TSPLIB.csv')

  # select only some of the instances (brazil58 == 17)
  selected = table_problems.iloc[:17, :].copy()

  # set the path to the instance files
  Problem.files_path = '30 selected instances/'

  # get the start time of loading the instances
  start_time = time.time()
  # load the instances
  problems = [Problem(name) for name in selected['Nome da Instância']]
  # get the end time of loading the instances
  end_time = time.time()
  # get the name of the last instance
  print(problems[-1].instance_name)
  # print the time to load the instances
  print('Total time to load the instances: ', end_time-start_time, 'seconds')


  ### Get the optimum tour, if exists ###


  # for problem in problems:
  #   print('Problem: ', problem.instance_name)  
  #   if problem.opt_tour is not None:
  #     opt_solve = Solve(problem.size, problem.opt_tour)
  #     print('    Optimum tour:', opt_solve, 'cost:', problem.evaluate(opt_solve))  
  #   else:
  #     print('    Optimum tour not known!')


  ### Generate a random tour, and perform a local search on it ###


  random_tours = []
  local_search_tours = []
  for problem in problems:
    # print('Problem: ', problem.instance_name)  
    random_tour = problem.random_solve(seed)
    random_cost = problem.evaluate(random_tour)
    # print('    random tour:', random_tour)
    # print('    random tour cost:', random_cost)
    random_tours.append(random_cost)

    local_search = LocalSearch(problem)
    local_search_tour = local_search.search(random_tour, 1)
    local_search_cost = problem.evaluate(local_search_tour)
    # print('    local_search tour:', local_search_tour)
    # print('    local_search tour cost:', local_search_cost)
    local_search_tours.append(local_search_cost)

  selected['Random on Seed '+str(seed)] = random_tours
  selected['LocalSearch on Random'] = local_search_tours


  ### Generate a greed search ###


  greeds = []
  greeds_tours = []
  for problem in problems:
    # print('Problem: ', problem.instance_name)  
    start_time = time.time()
    greed_tour = GreedSearch.search(problem)
    end_time = time.time()
    greed_cost = problem.evaluate(greed_tour)
    # print('    Time to run greed search: ', end_time-start_time, 'seconds')
    # print('    greed tour:', greed_tour)
    # print('    greed tour cost:', greed_cost)
    greeds.append(greed_cost)
    greeds_tours.append(greed_tour)
  selected['GreedSearch'] = greeds


  ### Run VNS on the instances in parallel ###


  reversed_problems = list(reversed(problems))
  reversed_greed_solves = list(reversed(greeds_tours))
  vns_inputs = [(problem, 4, 500, 250, max_exec_time_per_run_in_seconds, reversed_greed_solves[i]) for i, problem in enumerate(reversed_problems)]
  vns = []
  start_time = time.time()
  with multiprocessing.Pool(n_cores) as p:
    vns = p.map(simple_vns_run, vns_inputs)
  end_time = time.time()
  # print(vns)
  # times_vns = [(vals[1],i) for i, vals in enumerate(vns)]
  # choosed = max(times_vns)
  # print(choosed)
  # print(vns[choosed[1]], problems[choosed[1]].instance_name)
  print('Total time to run vns: ', end_time-start_time, 'seconds')
  selected['VNS Cost'] = [vals[0] for vals in reversed(vns)]
  selected['VNS Time'] = [vals[1] for vals in reversed(vns)]
  selected['VNS Iters'] = [vals[3] for vals in reversed(vns)]
  selected['VNS No_Upt'] = [vals[4] for vals in reversed(vns)]


  ### Run GRASP on the instances in parallel ###


  grasp_inputs = [(problem, 0.0, 3, 1000, 500, 10, max_exec_time_per_run_in_seconds) for problem in reversed_problems]
  grasp = []
  start_time = time.time()
  with multiprocessing.Pool(n_cores) as p:
    grasp = p.map(simple_grasp_run, grasp_inputs)
  end_time = time.time()
  # print(grasp)
  # times_grasp = [(vals[1],i) for i, vals in enumerate(grasp)]
  # choosed = max(times_grasp)
  # print(choosed)
  # print(grasp[choosed[1]], problems[choosed[1]].instance_name)
  print('Total time to run grasp: ', end_time-start_time, 'seconds')
  selected['GRASP Cost'] = [vals[0] for vals in reversed(grasp)]
  selected['GRASP Time'] = [vals[1] for vals in reversed(grasp)]
  selected['GRASP Iters'] = [vals[3] for vals in reversed(grasp)]
  selected['GRASP No_Upt'] = [vals[4] for vals in reversed(grasp)]
  bests = []
  for i in selected.index:
    bests.append(min([
                      (selected.iloc[i,3],  0, 'Random'),
                      (selected.iloc[i,4],  0, 'Local Search'),
                      (selected.iloc[i,5],  0, 'Greed Search'),
                      (selected.iloc[i,6],  selected.iloc[i,7], 'VNS'),
                      (selected.iloc[i,10], selected.iloc[i,11], 'GRASP')
                    ]
                   )[2]
               )
  selected['BEST'] = bests
  selected['VNS Tour'] = [vals[2] for vals in reversed(vns)]
  selected['GRASP Tour'] = [vals[2] for vals in reversed(grasp)]
  selected.to_csv(result_file_name)
  sys.exit(0)
