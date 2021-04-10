from Problem import Problem
from GreedSearch import GreedSearch
from VNS import VariableNeighborhoodSearch

import pandas as pd
import time
import multiprocessing
import sys
import json 

  ## Define some functions to run VNS and GRASP


def simple_vns_run(args):
  problem, seed, k, max_it, no_upt, max_time, best_solve = args
  print('VNS Started: Problem: ', problem.instance_name)  
  vns = VariableNeighborhoodSearch(problem, seed, None)
  parameters:dict = {
    "k": k,
    "max_it": max_it,
    "no_upt": no_upt,
    "max_time": max_time,
    "start_solve":best_solve
  }
  start_time = time.time()
  vns_tour, step, last_update = vns.run(parameters)
  end_time = time.time()
  vns_cost = problem.evaluate(vns_tour)
  print('VNS Done: Problem: ', problem.instance_name)  
  return pd.DataFrame([[problem.instance_name, seed, vns_cost, end_time-start_time, step, last_update]], columns=['Problem', 'Seed', 'Cost', 'Time', 'Steps', 'Last Updt'])


  ### Start the main problem ###


if __name__== '__main__' :

  if len(sys.argv) != 8:
    print("É necessario informar:")
    print("O arquivo com a configuração sobre as instancias e seeds a serem usadas")
    print("O tamanho da vizinhança a ser considerada")
    print("O número máximo de iterações do algoritmo")
    print("O número máximo de iterações do algoritmo sem atualização")
    print("O tempo máximo de execução de cada algoritmo em uma instancia, em segundos")
    print("O número máximo de execuções que podem rodar em paralelo")
    print("O nome do arquivo de saida com os resultados dos algoritmos")
    sys.exit(1)

  ### Set the seed to the random number generator ###
  ### Set the max time per run of algorithm ###
  ### Get the number of available cores ###

  with open(sys.argv[1]) as f:
    config = json.load(f)
  k_neighborhood = int(sys.argv[2])
  max_iterations = int(sys.argv[3])
  max_iterations_without_update = int(sys.argv[4])
  max_exec_time_per_run_in_seconds = float(sys.argv[5])
  n_cores = int(sys.argv[6])
  result_file_name = sys.argv[7]

  ### Load instance list ###

  # set the path to the instance files
  Problem.files_path = '30 selected instances/'
  # get the start time of loading the instances
  start_time = time.time()
  # load the instances
  problems = [Problem(x) for x in config["instances"]]
  # get the end time of loading the instances
  end_time = time.time()
  # print the time to load the instances
  print('Total time to load the instances: ', end_time-start_time, 'seconds')
  selected = pd.DataFrame([[p.size,p.opt_cost] for p in problems], columns=['Size', 'Opt Cost'], index=[p.instance_name for p in problems])
  print(selected.head())

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

  ### Run VNS on the instances in parallel ###

  reversed_problems = list(reversed(problems))
  reversed_greed_solves = list(reversed(greeds_tours))
  vns_inputs = [(problem, seed, k_neighborhood, max_iterations, max_iterations_without_update, max_exec_time_per_run_in_seconds, reversed_greed_solves[i]) for seed in config["seeds"] for i, problem in enumerate(reversed_problems)]
  vns = []
  print("Number of inputs:", len(vns_inputs))
  start_time = time.time()
  with multiprocessing.Pool(n_cores) as p:
    vns = p.map(simple_vns_run, vns_inputs)
  end_time = time.time()
  print('Total time to run vns: ', end_time-start_time, 'seconds')
  all_data = pd.concat(vns)

  def opt_dev(row):
    return abs(row['Cost'] - selected.loc[row['Problem'],'Opt Cost'])

  all_data['Opt_deviation'] = all_data.apply(opt_dev, axis=1)
  all_data.to_csv("all_"+result_file_name, index=False)
  gr = all_data.groupby(["Problem"])[["Cost", "Time", "Opt_deviation"]].agg({'Cost':['mean', 'std'], 'Time':['mean', 'std'], 'Opt_deviation':['mean', 'std'],})
  r = selected.join(gr)
  r.to_csv("results_"+result_file_name, index=True)
  sys.exit(0)
