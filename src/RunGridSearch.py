from Problem import Problem
from GridSearch import GridSearch
from GreedSearch import GreedSearch

from Genetic import Genetic
from VNS import VariableNeighborhoodSearch
from GRASP import GRASP

import json
import pandas as pd
import time
import sys

if __name__== '__main__' :
  if len(sys.argv) != 6:
    print("É necessario informar:")
    print("O arquivo com a configuração geral do GridSearch: as instancias e seeds a serem usadas")
    print("O nome do algoritmo a ser usado no GridSearch")
    print("O arquivo com as configurações possiveis do algoritmo a ser usado no GridSearch")
    print("O número máximo de execuções que podem rodar em paralelo")
    print("O nome do arquivo de saida com os resultados")
    sys.exit(1)

  with open(sys.argv[1]) as f:
    config = json.load(f)
  with open(sys.argv[3]) as f:
    parameters = json.load(f)

  if sys.argv[2] == "genetic":
    alg = Genetic(None, None)
  elif sys.argv[2] == "vns":
    alg = VariableNeighborhoodSearch(None, None, None)
  elif sys.argv[2] == "grasp":
    alg = GRASP(None, None, None)
  else:
    print("O nome do algoritmo informado é inválido, escolhar entre: 'genetic', 'vns' e 'grasp'")
    sys.exit(1)

  n_cores = int(sys.argv[4])
  result_file_name = sys.argv[5]

  Problem.files_path = '30 selected instances/'
  
  problems = [Problem(x) for x in config["instances"]]
  
  grid = GridSearch(
    n_cores,
    alg,
    problems,
    [GreedSearch.search(p) for p in problems],
    config["seeds"],
    parameters
  )

  start = time.time()
  grid.start()
  end = time.time()
  
  print("Total Time: ", end-start)

  df = pd.DataFrame.from_dict(grid.parametersRanks)
  df = df.transpose()
  parameters_name = sorted(list(parameters.keys()))
  df.index.set_names(parameters_name, inplace=True)
  df.to_csv("ranks_"+result_file_name)

  df = pd.DataFrame.from_dict(grid.bestSolves, orient='index')
  df.to_csv("bests_"+result_file_name)

  df = pd.DataFrame.from_dict(grid.results)
  df = df.transpose()
  parameters_name.append("instance_name")
  parameters_name.append("seed")
  df.index.set_names(parameters_name, inplace=True)
  df.to_csv("means_"+result_file_name)
  