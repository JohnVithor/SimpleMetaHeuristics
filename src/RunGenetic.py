from Problem import Problem
from GreedSearch import GreedSearch
from Genetic import Genetic

import pandas as pd
import time
import multiprocessing
import sys

seed = 0
max_exec_time_per_run_in_minutes = 1
max_exec_time_per_run_in_seconds = 60.0 * max_exec_time_per_run_in_minutes
n_cores = 1
result_file_name = "genetic_results.csv"


  ## Define some functions to run Genetic


def simple_genetic_run(args):
  global seed
  problem, contest_size, cross_rate, mutate_rate, size, epochs, max_time, best_solve = args
  print('Genetic Started: Problem: ', problem.instance_name)  
  genetic = Genetic(problem, seed)
  start_time = time.time()
  genetic_tour, step = genetic.run(contest_size, cross_rate, mutate_rate, size, epochs, max_time, best_solve)
  end_time = time.time()
  genetic_cost = problem.evaluate(genetic_tour)
  print('Genetic Done: Problem: ', problem.instance_name)  
  return genetic_cost, end_time-start_time, genetic_tour, step


  ### Start the main problem ###


if __name__== '__main__' :

  if len(sys.argv) != 11:
    print("É necessario informar:")
    print("A quantidade de instancias a serem avaliadas")
    print("A seed para gerar os números aleatorios")
    print("A quantidade de soluções a serem consideradas como candidatas do crossover")
    print("A taxa de crossover")
    print("A taxa de mutação")
    print("O tamanho da população")
    print("A quantidade de epocas/iterações do algoritmo")
    print("O tempo máximo de execução de cada algoritmo em uma instancia, em minutos")
    print("O número máximo de execuções que podem rodar em paralelo")
    print("O nome do arquivo de saida com os resultados dos algoritmos")
    sys.exit(1)

  ### Set the seed to the random number generator ###
  ### Set the max time per run of algorithm ###
  ### Get the number of available cores ###

  qtd_instancias = int(sys.argv[1])
  seed = int(sys.argv[2])
  contest_size = int(sys.argv[3])
  cross_rate = float(sys.argv[4])
  mutate_rate = float(sys.argv[5])
  pop_size = int(sys.argv[6])
  epochs = int(sys.argv[7])
  max_exec_time_per_run_in_minutes = float(sys.argv[8])
  max_exec_time_per_run_in_seconds = 60.0 * max_exec_time_per_run_in_minutes
  n_cores = int(sys.argv[9])
  result_file_name = sys.argv[10]


  ### Load instance list ###


  table_problems = pd.read_csv('TSP - PCV Instancias TSPLIB.csv')

  # select only some of the instances (brazil58 == 17)
  selected = table_problems.iloc[:17, :].copy()

  # set the path to the instance files
  Problem.files_path = '30 selected instances/'

  # get the start time of loading the instances
  start_time = time.time()
  # load the instances
  problems = [Problem(name) for name in selected['Nome']]
  # get the end time of loading the instances
  end_time = time.time()
  # get the name of the last instance
  print(problems[-1].instance_name)
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


  ### Run Genetic on the instances in parallel ###


  reversed_problems = list(reversed(problems))
  reversed_greed_solves = list(reversed(greeds_tours))
  gene_inputs = [(problem, contest_size, cross_rate, mutate_rate, pop_size, epochs, max_exec_time_per_run_in_seconds, reversed_greed_solves[i]) for i, problem in enumerate(reversed_problems)]
  genetic = []

  start_time = time.time()
  with multiprocessing.Pool(n_cores) as p:
    genetic = p.map(simple_genetic_run, gene_inputs)
  end_time = time.time()

  print('Total time to run genetic: ', end_time-start_time, 'seconds')
  selected['Genetic Cost'] = [vals[0] for vals in reversed(genetic)]
  selected['Genetic Time'] = [vals[1] for vals in reversed(genetic)]
  selected['Genetic Tour'] = [vals[2] for vals in reversed(genetic)]
  selected['Genetic Iters'] = [vals[3] for vals in reversed(genetic)]

  selected.to_csv(result_file_name, index=False)
  sys.exit(0)
