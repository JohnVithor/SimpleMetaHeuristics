from Problem import Problem
from Solve import Solve
from AlgorithmInterface import AlgorithmInterface

from mergedeep import merge

import numpy as np
import time
from typing import List
from multiprocessing import Process, Queue, Pool, Manager

class GridSearch:
  def __init__(self, pool_size:int, algorithm:AlgorithmInterface, instances:List[Problem], start_solves:List[Solve], seeds:List[int], parameters_grid:dict):
    self.algorithm = algorithm
    self.instances = instances
    self.seeds = seeds
    self.parameters_grid = parameters_grid
    self.start_solves = {x.instance_name:start_solves[i] for i,x in enumerate(self.instances)}
    self.mapping = {count:key for count, key in enumerate(list(self.parameters_grid.keys()))}
    self.size:int = len(self.parameters_grid.keys())
    self.bestSolves = {x.instance_name:[x.random_solve(self.seeds[0]),frozenset({})] for x in self.instances}
    self.bestsMeanParameter = {}
    self.parametersRanks = []
    self.results = {}
    self.pool = Pool(pool_size)
    self.tasks = []
    self.m = Manager()
    self.total_runs = np.prod([len(parameters_grid[x]) for x in parameters_grid])
    self.counter = 1

  def aaevaluate(self, parameters:dict):
    key = frozenset(parameters.items())
    self.results[key] = {}
    for p in self.instances:
      print("Evaluating: ", key, " on instance ", p.instance_name)
      self.results[key][p.instance_name] = {}
      costs_sum = 0
      times_sum = 0
      for s in self.seeds:
        local_alg = self.algorithm.copy()
        local_alg.seed = s
        local_alg.problem = p
        parameters['best_solve'] = self.start_solves[p.instance_name]
        initial_time = time.time()
        solve, *others = local_alg.run(parameters)
        final_time = time.time()
        total_time = final_time-initial_time
        self.results[key][p.instance_name][s] = {"solve":solve, "others":others, "time":total_time}
        costs_sum += solve.cost
        times_sum += total_time
        print("With seed ", s, " cost: ", solve.cost, " time: ", total_time)
        if(solve.cost < self.bestSolves[p.instance_name][0].cost):
          self.bestSolves[p.instance_name][0] = solve
          self.bestSolves[p.instance_name][1] = key
      self.results[key][p.instance_name]["mean"] = {"cost":float(costs_sum)/len(self.seeds), "time":float(times_sum)/len(self.seeds)}
    return "done"

  @staticmethod
  def evaluate(counter, max_counter, algorithm, parameters:dict, instances, seeds, start_solves, bestSolves):
    print("Started Iteration ", counter, "of ", max_counter)
    key = frozenset(parameters.items())
    results = {}
    results[key] = {}
    for p in instances:
      # print("Evaluating: ", key, " on instance ", p.instance_name)
      results[key][p.instance_name] = {}
      costs_sum = 0
      times_sum = 0
      for s in seeds:
        local_alg = algorithm.copy()
        local_alg.seed = s
        local_alg.problem = p
        parameters['best_solve'] = start_solves[p.instance_name]
        initial_time = time.time()
        solve, *others = local_alg.run(parameters)
        final_time = time.time()
        total_time = final_time-initial_time
        results[key][p.instance_name][s] = {"cost":solve, "others":others, "time":total_time}
        costs_sum += solve.cost
        times_sum += total_time
        if(solve.cost < bestSolves[p.instance_name][0].cost):
          bestSolves[p.instance_name][0] = solve
          bestSolves[p.instance_name][1] = key
      results[key][p.instance_name]["mean"] = {"cost":float(costs_sum)/len(seeds), "time":float(times_sum)/len(seeds)}
    print("Finalized Iteration ", counter, "of ", max_counter)
    return results, bestSolves


  def order(self):
    print("Ordering Results Start")
    size = len(self.results.keys())
    for p in self.instances:
      params_for_p = [[k,self.results[k][p.instance_name]["mean"]] for k in self.results.keys()]
      self.bestsMeanParameter[p.instance_name] = sorted(params_for_p, key=lambda x: (x[1]['cost'], x[1]['time']))
    for k in self.results.keys():
      cumulative_rank = 0
      best_rank = size
      worst_rank = 0
      for p in self.instances:
        for j, v in enumerate(self.bestsMeanParameter[p.instance_name]):
          if k == v[0]:
            cumulative_rank += j
            if j < best_rank:
              best_rank = j
            if j > worst_rank:
              worst_rank = j
            break
      new_key = tuple([x[1] for x in sorted(list(k))])
      self.parametersRanks.append((new_key, (float(cumulative_rank)/size, worst_rank, best_rank, cumulative_rank)))
    self.parametersRanks = sorted(self.parametersRanks, key=lambda x: x[1])
    self.parametersRanks = {p[0]:{'mean_rank':p[1][0], 'worst_rank':p[1][1], 'best_rank':p[1][2], 'cumulative_rank':p[1][3]} for p in self.parametersRanks}
    temp_results = {}
    for k in self.results.keys():
      new_key = [x[1] for x in sorted(list(k))]
      new_key.append('problem')
      new_key.append('seed')
      for p in self.results[k]:
        new_key[-2] = p
        for s in self.results[k][p]:
          new_key[-1] = s
          temp_results[tuple(new_key)] = self.results[k][p][s]
    self.results = temp_results 
    print("Ordering Results Done")

  def start(self):
    current:list = [0]*self.size
    for i in range(self.size):
      current[i] = self.parameters_grid[self.mapping[i]][0]
    self.run(0, current)
    self.pool.close()
    self.pool.join()
    r = [t.get() for t in self.tasks]
    [merge(self.results,a[0]) for a in r]
    
    for p in self.instances:
      for a in r:
        if a[1][p.instance_name][0].cost < self.bestSolves[p.instance_name][0].cost:
          self.bestSolves[p.instance_name][0] = a[1][p.instance_name][0]
          self.bestSolves[p.instance_name][1] = a[1][p.instance_name][1]
      params = {x[0]:x[1] for x in self.bestSolves[p.instance_name][1]}
      params['cost'] = self.bestSolves[p.instance_name][0].cost
      self.bestSolves[p.instance_name] = params
    self.order()

  def run(self, idx:int, current:list):
    if idx == len(current):
      params = {self.mapping[i]:current[i] for i in range(len(current))}
      self.tasks.append(self.pool.apply_async(GridSearch.evaluate, (self.counter, self.total_runs, self.algorithm, params,self.instances, self.seeds, self.start_solves, self.bestSolves)))
      self.counter += 1
    if idx < len(current):
      for v in self.parameters_grid[self.mapping[idx]]:
        copy = current[:]
        copy[idx] = v
        self.run(idx + 1, copy)
