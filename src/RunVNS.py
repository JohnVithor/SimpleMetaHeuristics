from Problem import Problem
from GreedSearch import GreedSearch
from VNS import VariableNeighborhoodSearch

import pandas as pd
import time
import multiprocessing
import sys

seed = 0
max_exec_time_per_run_in_minutes = 1
max_exec_time_per_run_in_seconds = 60.0 * max_exec_time_per_run_in_minutes
n_cores = 1
result_file_name = "vns_results.csv"


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
  print('VNS Done: Problem: ', problem.instance_name)  
  return vns_cost, end_time-start_time, vns_tour, step, last_update


  ### Start the main problem ###


if __name__== '__main__' :

  if len(sys.argv) != 9:
    print("É necessario informar:")
    print("A quantidade de instancias a serem avaliadas")
    print("A seed para gerar os números aleatorios")
    print("O tamanho da vizinhança a ser considerada")
    print("O número máximo de iterações do algoritmo")
    print("O número máximo de iterações do algoritmo sem atualização")
    print("O tempo máximo de execução de cada algoritmo em uma instancia, em minutos")
    print("O número máximo de execuções que podem rodar em paralelo")
    print("O nome do arquivo de saida com os resultados dos algoritmos")
    sys.exit(1)

  ### Set the seed to the random number generator ###
  ### Set the max time per run of algorithm ###
  ### Get the number of available cores ###

  qtd_instancias = int(sys.argv[1])
  seed = int(sys.argv[2])
  k_neighborhood = int(sys.argv[3])
  max_iterations = int(sys.argv[4])
  max_iterations_without_update = int(sys.argv[5])
  max_exec_time_per_run_in_minutes = float(sys.argv[6])
  max_exec_time_per_run_in_seconds = 60.0 * max_exec_time_per_run_in_minutes
  n_cores = int(sys.argv[7])
  result_file_name = sys.argv[8]


  ### Load instance list ###


  table_problems = pd.read_csv('TSP - PCV Instancias TSPLIB.csv')

  # select only some of the instances
  selected = table_problems.iloc[:qtd_instancias, :].copy()

  # set the path to the instance files
  Problem.files_path = '30 selected instances/'

  # get the start time of loading the instances
  start_time = time.time()
  # load the instances
  problems = [Problem(name) for name in selected['Nome']]
  # get the end time of loading the instances
  end_time = time.time()
  # get the name and size of the last instance
  print(problems[-1].instance_name, problems[-1].size)
  # print the time to load the instances
  print('Total time to load the instances: ', end_time-start_time, 'seconds')


  ### Generate a greed search ###


  greeds = []
  greeds_tours = []
  for problem in problems:
    start_time = time.time()
    greed_tour = GreedSearch.search(problem)
    end_time = time.time()
    greed_cost = problem.evaluate(greed_tour)
    greeds.append(greed_cost)
    greeds_tours.append(greed_tour)
  selected['Greed Cost'] = greeds
  selected['Greed Tour'] = [vals for vals in greeds_tours]


  ### Run VNS on the instances in parallel ###


  reversed_problems = list(reversed(problems))
  reversed_greed_solves = list(reversed(greeds_tours))
  vns_inputs = [(problem, k_neighborhood, max_iterations, max_iterations_without_update, max_exec_time_per_run_in_seconds, reversed_greed_solves[i]) for i, problem in enumerate(reversed_problems)]
  vns = []

  start_time = time.time()
  with multiprocessing.Pool(n_cores) as p:
    vns = p.map(simple_vns_run, vns_inputs)
  end_time = time.time()

  print('Total time to run vns: ', end_time-start_time, 'seconds')
  selected['VNS Cost'] = [vals[0] for vals in reversed(vns)]
  selected['VNS Time'] = [vals[1] for vals in reversed(vns)]
  selected['VNS Tour'] = [vals[2] for vals in reversed(vns)]
  selected['VNS Iters'] = [vals[3] for vals in reversed(vns)]
  selected['VNS No_Upt'] = [vals[4] for vals in reversed(vns)]

  selected.to_csv(result_file_name, index=False)
  sys.exit(0)
