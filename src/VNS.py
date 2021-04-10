from Problem import Problem
from Solve import Solve
from LocalSearch import LocalSearch
from AlgorithmInterface import AlgorithmInterface

import random
import time
import sys

class VariableNeighborhoodSearch(AlgorithmInterface):
  def __init__(self, problem:Problem, seed:int=0, searcher:LocalSearch=None ):
    AlgorithmInterface.__init__(self, problem, seed)
    self.searcher = searcher
    if searcher is None:
      self.searcher = LocalSearch(problem)
    random.seed(self.seed)
    self.actual_k = 1
    self.explored = {}

  def copy(self):
    return VariableNeighborhoodSearch(self.problem, self.seed, self.searcher)

  def run(self, parameters:dict) -> Solve:
    max_k:int = parameters["max_k"] if "max_k" in parameters else 3
    max_steps:int = parameters["max_steps"] if "max_steps" in parameters else 30
    no_update:int = parameters["no_update"] if "no_update" in parameters else 10
    max_time:float = parameters["max_time"] if "max_time" in parameters else 60.0
    start_solve:Solve = parameters["start_solve"] if "start_solve" in parameters else None
    random.seed(self.seed)
    if start_solve is not None:
      best_solve = start_solve.copy()
    else:
      p_seed = random.randint(-max_steps,max_steps)
      old_state = random.getstate()
      best_solve : Solve = self.problem.random_solve(p_seed)
      random.setstate(old_state)
    solve:Solve = best_solve.copy()
    step = 0
    last_update = 0
    initial_time = time.time()
    end_time = time.time()
    while step < max_steps and (step - last_update) <= no_update and (end_time - initial_time) <= max_time:
      if self.actual_k > max_k:
        self.explored[solve] = True
        p_seed = random.randint(-max_steps,max_steps)
        old_state = random.getstate()
        solve : Solve = self.problem.random_solve(p_seed)
        random.setstate(old_state)
        if solve in self.explored.keys() and self.explored[solve] == True:
          continue
        self.actual_k = 1
      self.explored[solve] = False
      solve : Solve = self.get_first_best_neighbor(solve, self.actual_k, initial_time, max_time)
      if self.problem.evaluate(solve) < self.problem.evaluate(best_solve):
        self.actual_k = 1
        best_solve = solve.copy()
        last_update = step
      else:
        self.actual_k = self.actual_k + 1
      step += 1
      end_time = time.time()
    return best_solve, step, last_update

  def get_first_best_neighbor(self, solve:Solve, k:int, initial_time:int, max_time:int) -> Solve:
    best_solve = solve.copy()
    neighborhood = self.searcher.set_neighborhood_1_k(solve, k, initial_time, max_time)
    for neigh in neighborhood:
      if self.problem.evaluate(neigh) < self.problem.evaluate(best_solve):
        return neigh.copy()
    return best_solve
