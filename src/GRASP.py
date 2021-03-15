from Problem import Problem
from Solve import Solve
import random
from LocalSearch import LocalSearch
import time

class GRASP:
  def __init__(self, problem:Problem, searcher:LocalSearch = None, seed:int=0):
    self.problem = problem
    self.local_search = searcher
    self.frequent_links = {}
    self.links = {}
    if searcher is None:
      self.local_search = LocalSearch(self.problem)
    self.original_seed = seed
    self.seed = seed
    random.seed(self.original_seed)
  

  def run(self, alpha:float=0.1, k:int=2, max_steps:int=100, no_update:int=50, start_incr:int=10, max_time:float=60.0, start_solve:Solve = None) -> Solve:
    random.seed(self.original_seed)
    start_alpha = alpha
    if start_solve is not None:
      best_solve = start_solve.copy()
    else:
      best_solve : Solve = self.make_solve(alpha)

    step = 0
    last_update = 0
    
    initial_time = time.time()
    end_time = time.time()
    
    while step < max_steps and (step - last_update) <= no_update and (end_time - initial_time) <= max_time:

      if step - last_update >= start_incr:
        alpha += 0.05
        alpha = min(alpha, 1.0)
             
      solve : Solve = self.make_solve(alpha)
      solve = self.local_search.search(solve, k)

      if self.problem.evaluate(solve) < self.problem.evaluate(best_solve):
        best_solve = solve
        alpha = start_alpha
        last_update = step

      step +=1
      end_time = time.time()

    return best_solve, step, last_update

  def make_solve(self, alpha:float) -> Solve:
    tour = [0] * self.problem.size
    used = [False] * self.problem.size
    
    tour[0] = random.randint(1, self.problem.size)
    used[tour[0]-1] = True

    total_cost = 0
    next_position = 1
    actual_node = tour[0]-1
    best_candidate = 0
    
    first_min_element = True
    first_max_element = True
    min_cost = 0
    max_cost = 0

    elements = []

    while tour[self.problem.size-1] == 0:
      elements = []
      first_min_element = True
      first_max_element = True
      min_cost = 0
      max_cost = 0

      for i in range(self.problem.size):
        if not used[i] and i != actual_node:
          elements.append(i)
          
          if (first_min_element or self.problem.distance_matrix[actual_node,i] < min_cost):
            min_cost = self.problem.distance_matrix[actual_node,i]
            first_min_element = False
          
          if (first_max_element or self.problem.distance_matrix[actual_node,i] > max_cost):
            max_cost = self.problem.distance_matrix[actual_node,i]
            first_max_element = False

      lcr = []
      for candidate in elements:
        cost = self.problem.distance_matrix[actual_node, candidate]
        if cost >= min_cost and cost <= min_cost + alpha * (max_cost - min_cost):
          lcr.append((candidate, cost))           

      if len(lcr) != 0:
        lcr_pos = 0 if len(lcr) == 1 else random.randint(0, len(lcr)-1)
        choosed, choosed_cost = lcr[lcr_pos]
      else:
        ele_pos = 0 if len(elements) == 1 else random.randint(0, len(elements)-1)
        choosed, choosed_cost = elements[ele_pos], self.problem.distance_matrix[actual_node, elements[ele_pos]]

      tour[next_position] = choosed+1
      next_position += 1
      total_cost += choosed_cost
      used[choosed] = True
      actual_node = choosed

    total_cost += self.problem.distance_matrix[actual_node,0]
    solve = Solve(self.problem.size, tour)
    solve.cost = total_cost
    return solve