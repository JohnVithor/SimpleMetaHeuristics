from Problem import Problem
from Solve import Solve
import random
import time
from LocalSearch import LocalSearch
import sys


class VariableNeighborhoodSearch:
  def __init__(self, problem:Problem, searcher:LocalSearch = None, seed:int=0):
    self.problem = problem
    self.local_search = searcher
    if searcher is None:
      self.local_search = LocalSearch(problem)
    self.original_seed = seed
    random.seed(self.original_seed)
    self.actual_k = 1
    self.explored = {}

  def run(self, max_k:int=3, max_steps:int=30, no_update:int=10, max_time:float=60.0, start_solve:Solve = None) -> Solve:
    random.seed(self.original_seed)
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
    neighborhood = self.local_search.set_neighborhood_1_k(solve, k, initial_time, max_time)
    for neigh in neighborhood:
      if self.problem.evaluate(neigh) < self.problem.evaluate(best_solve):
        return neigh.copy()

    return best_solve
