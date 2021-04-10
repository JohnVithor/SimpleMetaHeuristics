import pandas as pd
import time
import sys

result_file_name = "best_results.csv"
number_of_instances = 1

  ### Start the main problem ###

if __name__== '__main__' :
  if len(sys.argv) < 4:
    print("É necessario informar:")
    print("A quantidade de instâncias as serem avaliadas em cada arquivo")
    print("Os arquivos que seram utilizados para comparar qual o melhor algoritmo")
    print("O nome do arquivo de saida com o resultado da comparação")
    sys.exit(1)

  ### Set the seed to the random number generator ###
  ### Set the max time per run of algorithm ###
  ### Get the number of available cores ###

  number_of_instances = int(sys.argv[1])
  result_file_name = sys.argv[-1]

  sub_cost = "Cost"
  sub_time = "Time"
  costs_time_ids = []
  total_data = pd.DataFrame()
  for i in range(2,len(sys.argv)-1):
    file_results = pd.read_csv(sys.argv[i])[:number_of_instances]
    # total_data = pd.concat([total_data, file_results], axis=1)
    f_cost = [s for s in file_results.columns if sub_cost in s]
    f_time = [s for s in file_results.columns if sub_time in s]
    costs_time_id = list(zip(file_results[f_cost[1]], file_results[f_time[0]], [sys.argv[i]]*number_of_instances))
    costs_time_ids.append(costs_time_id)
  

  ### Get Greed results ###

  file_results = pd.read_csv(sys.argv[2])[:number_of_instances]
  cost = [s for s in file_results.columns if sub_cost in s]
  costs_time_id = list(zip(file_results[cost[0]], [0]*number_of_instances, ["Greed Search"]*number_of_instances))
  costs_time_ids.append(costs_time_id)
  
  total_data['Nome'] = file_results["Nome"]
  total_data['Tamanho'] = file_results["Tamanho"]
  total_data['Melhor custo conhecido'] = file_results["Melhor custo conhecido"]

  ### Compare results ###

  start_time = time.time()
  bests = []
  bests_cost = []
  for i in range(number_of_instances):
    vals_i = []
    for j in range(len(costs_time_ids)):
      vals_i.append(costs_time_ids[j][i])
    bests.append(min(vals_i)[2])
    bests_cost.append(min(vals_i)[0])
  end_time = time.time()

  print('Total time to compare results: ', end_time-start_time, 'seconds')

  total_data['Best'] = bests
  total_data['Cost'] = bests_cost
  total_data.to_csv(result_file_name, index=False)
  sys.exit(0)
