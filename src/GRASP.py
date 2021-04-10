from Problem import Problem
from Solve import Solve
from LocalSearch import LocalSearch
from AlgorithmInterface import AlgorithmInterface

import random
import time

class GRASP(AlgorithmInterface):
  """
  Greedy Randomized Adaptative Search Procedure (GRASP)
  Esta classe implementa uma metaheuristica para o Problema do Caixeiro Viajante

  Atributos
    ----------
    name : str
        first name of the person
    surname : str
        family name of the person
    age : int
        age of the person

  Métodos
    -------
    info(additional=""):
        Prints the person's name and age.

  """
  def __init__(self, problem:Problem, seed:int=0, searcher:LocalSearch=None):
    """
    Construtor da classe GRASP, aqui são informados a instancia do problema do caixeiro 
    viajante a ser utilizada e opcionalmente qual o objeto de Busca Local e semente de 
    geração de números aleátorios que serão usadas.

    Caso nenhum objeto de Busca Local seja especificado, é criado um LocalSeacher simples
    para ser utilizado.

    :param problem: Problem
    :param seed: int = 0
    :param searcher: LocalSearch = None
    """
    AlgorithmInterface.__init__(self, problem, seed)
    self.local_search = searcher
    if searcher is None:
      self.local_search = LocalSearch(self.problem)
  

  def copy(self):
    return GRASP(self.problem, self.seed, self.searcher)


  def run(self, parameters:dict) -> Solve:
    alpha:float = parameters["alpha"] if "alpha" in parameters else 0.1
    k:int = parameters["k"] if "k" in parameters else 2
    max_steps:int = parameters["max_steps"] if "max_steps" in parameters else 100
    no_update:int = parameters["no_update"] if "no_update" in parameters else 50
    start_incr:int = parameters["start_incr"] if "start_incr" in parameters else 10
    max_time:float = parameters["max_time"] if "max_time" in parameters else 60.0
    start_solve:Solve = parameters["start_solve"] if "start_solve" in parameters else None
    random.seed(self.seed)
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
