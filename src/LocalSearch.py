from Problem import Problem
from Solve import Solve
import networkx as nx
import sys
import time

class LocalSearch:
  def __init__(self, problem:Problem, max_size_stored_neighborhood: int=104_857_600):
    self.known_set_neighborhood = {}
    self.problem = problem
    self.max_size_stored_neighborhood = max_size_stored_neighborhood
    self.mem_size = 0 

  def search(self, solve:Solve, k:int = 1) -> Solve:
    best_solve = solve.copy()

    for neigh in self.set_neighborhood_1_k(solve, k):
      if self.problem.evaluate(neigh) < self.problem.evaluate(best_solve):
        best_solve = neigh.copy()

    if self.problem.evaluate(best_solve) < self.problem.evaluate(best_solve):
      return self.search(best_solve, k)
    else:
      return best_solve

  def set_neighborhood_1_k(self, solve:Solve, k:int, initial_time:int = -1, max_time:int = -1) -> set:
    if k == 0:
      return set()
    if self.known_set_neighborhood is None:
      self.known_set_neighborhood = {}
    if (solve, k) in self.known_set_neighborhood.keys():
      return self.known_set_neighborhood[(solve, k)]

    if self.mem_size >= self.max_size_stored_neighborhood:
      self.known_set_neighborhood.clear()
      self.mem_size = 0

    imediate_solves : list = []
    for i in range(solve.size-1):
      neigh = solve.copy()
      aux = neigh.tour[i]
      neigh.tour[i] = neigh.tour[i+1]
      neigh.tour[i+1] = aux
      imediate_solves.append(neigh)

    neigh = solve.copy()
    aux = neigh.tour[0]
    neigh.tour[0] = neigh.tour[-1]
    neigh.tour[-1] = aux
    imediate_solves.append(neigh)

    final_solves = set(imediate_solves)
    for s in imediate_solves:
      if (s, k) in self.known_set_neighborhood.keys():
        set_s = self.known_set_neighborhood[(s, k)]
      else:
        set_s = self.set_neighborhood_1_k(s, k-1, initial_time, max_time)
      final_solves = final_solves.union(set_s)
      if (max_time > 0 and (time.time() - initial_time) > max_time):
        break
    
    final_solves = frozenset(final_solves)
    self.known_set_neighborhood[(solve, k)] = final_solves
    self.mem_size += sys.getsizeof(final_solves)
    return final_solves