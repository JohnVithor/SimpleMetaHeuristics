from Problem import Problem
from Solve import Solve

class GreedSearch:
  @staticmethod
  def search(problem:Problem) -> Solve:
    tour = [0] * problem.size
    used = [False] * problem.size
    tour[0] = 1
    used[0] = True
    total_cost = 0
    next_position = 1
    actual_node = 0
    best_candidate = 0
    first_element = True
    minor_cost = 0
    while tour[problem.size-1] == 0:
      first_element = True
      minor_cost = 0
      for i in range(problem.size):
        if (not used[i]) and (first_element or problem.distance_matrix[actual_node,i] < minor_cost):
          minor_cost = problem.distance_matrix[actual_node,i]
          first_element = False
          best_candidate = i
      tour[next_position] = best_candidate+1
      next_position += 1
      total_cost += minor_cost
      used[best_candidate] = True
      actual_node = best_candidate
    total_cost += problem.distance_matrix[actual_node,0]
    return Solve(problem.size, tour)
