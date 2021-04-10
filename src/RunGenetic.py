from Problem import Problem
from GreedSearch import GreedSearch
from Genetic import Genetic

import pandas as pd
import time
import multiprocessing
import sys
import json

  ## Define some functions to run Genetic


def simple_genetic_run(args):
  problem, seed, contest_size, cross_rate, mutate_rate, size, epochs, max_time, best_solve = args
  print('Genetic Started: Problem: ', problem.instance_name)
  genetic = Genetic(problem, seed)
  parameters:dict = {
    "contest_size":contest_size,
    "cross_rate": cross_rate,
    "mutate_rate": mutate_rate,
    "size": size,
    "epochs": epochs,
    "max_time": max_time,
    "start_solve":best_solve
    }
  start_time = time.time()
  genetic_tour, step = genetic.run(parameters)
  end_time = time.time()
  genetic_cost = problem.evaluate(genetic_tour)
  print('Genetic Done: Problem: ', problem.instance_name)
  return pd.DataFrame([[problem.instance_name, seed, genetic_cost, end_time-start_time, step]], columns=['Problem', 'Seed', 'Cost', 'Time', 'Steps'])


  ### Start the main problem ###


if __name__== '__main__' :

  if len(sys.argv) != 10:
    print("É necessario informar:")
    print("O arquivo com a configuração sobre as instancias e seeds a serem usadas")
    print("A quantidade de soluções a serem consideradas como candidatas do crossover")
    print("A taxa de crossover")
    print("A taxa de mutação")
    print("O tamanho da população")
    print("A quantidade de epocas/iterações do algoritmo")
    print("O tempo máximo de execução de cada algoritmo em uma instancia, em segundos")
    print("O número máximo de execuções que podem rodar em paralelo")
    print("O nome do arquivo de saida com os resultados dos algoritmos")
    sys.exit(1)

  ### Set the seed to the random number generator ###
  ### Set the max time per run of algorithm ###
  ### Get the number of available cores ###

  with open(sys.argv[1]) as f:
    config = json.load(f)
  contest_size = int(sys.argv[2])
  cross_rate = float(sys.argv[3])
  mutate_rate = float(sys.argv[4])
  pop_size = int(sys.argv[5])
  epochs = int(sys.argv[6])
  max_exec_time_per_run_in_seconds = float(sys.argv[7])
  n_cores = int(sys.argv[8])
  result_file_name = sys.argv[9]

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

  ### Run Genetic on the instances in parallel ###

  reversed_problems = list(reversed(problems))
  reversed_greed_solves = list(reversed(greeds_tours))
  gene_inputs = [(problem, seed, contest_size, cross_rate, mutate_rate, pop_size, epochs, max_exec_time_per_run_in_seconds, reversed_greed_solves[i]) for seed in config["seeds"] for i, problem in enumerate(reversed_problems)]
  print("Number of inputs:", len(gene_inputs))
  start_time = time.time()
  with multiprocessing.Pool(n_cores) as p:
    genetic = p.map(simple_genetic_run, gene_inputs)
  end_time = time.time()
  print('Total time to run genetic: ', end_time-start_time, 'seconds')
  all_data = pd.concat(genetic)

  def opt_dev(row):
    return abs(row['Cost'] - selected.loc[row['Problem'],'Opt Cost'])

  all_data['Opt_deviation'] = all_data.apply(opt_dev, axis=1)
  all_data.to_csv("all_"+result_file_name, index=False)
  gr = all_data.groupby(["Problem"])[["Cost", "Time", "Opt_deviation"]].agg({'Cost':['mean', 'std'], 'Time':['mean', 'std'], 'Opt_deviation':['mean', 'std'],})
  r = selected.join(gr)
  r.to_csv("results_"+result_file_name, index=True)
  sys.exit(0)
