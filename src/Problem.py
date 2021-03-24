import random

import tsplib95
import numpy as np
import networkx as nx

from Solve import Solve

class Problem:
  """
  A classe Problem modela uma instância do Problema do Caixeiro Viajante
  
  Esta classe além de encapsular a 

  Atributos
    ----------
    size : int
      O Tamanho da solução
    cost : float
      O Custo da solução
    tour : list[int]
      Uma lista de inteiros com tamanho 'size' armazenando a ordem de visitação 
      dos nós (cidades) no problema.
  """

  files_path = ""
  tour_files_suffix = '.opt.tour'
  
  def __init__(self, instance_name:str, file_type:str='.tsp'):
    self.instance_name = instance_name

    if file_type == '.tsp':
      self.instance = tsplib95.load(Problem.files_path+self.instance_name+file_type)
      self.nx_graph = self.instance.get_graph()
      try:
        self.tour = tsplib95.load(Problem.files_path+self.instance_name+Problem.tour_files_suffix)
        self.opt_cost = self.instance.trace_tours(self.tour.tours)
        self.opt_tour = self.tour.tours[0]
      except:
        self.tour = None
        self.opt_cost = None
        self.opt_tour = None
    elif file_type == '.graphml':
      self.instance = None
      self.tour = None
      self.nx_graph = nx.read_graphml(Problem.files_path+self.instance_name+file_type)
      self.opt_cost = 0
      self.opt_tour = []

    self.distance_matrix = nx.to_numpy_matrix(self.nx_graph)  
    self.instance = None
    self.tour = None
    self.size = self.distance_matrix.shape[0]

  def evaluate(self, solve : Solve) -> float:
    if self.instance is not None:
      try:
        solve.cost = self.instance.trace_tours([solve.tour])[0]
        return solve.cost
      except:
        return self.manual_evaluate(solve)
    return self.manual_evaluate(solve)

  def manual_evaluate(self, solve:Solve) -> float:
    value : float = 0
    for pos in range(solve.size-1):
      s = solve.tour[pos] - 1
      e = solve.tour[pos+1] - 1 
      value += self.distance_matrix[s, e]

    value += self.distance_matrix[solve.tour[-1]-1, solve.tour[0]-1]
    solve.cost = value
    return solve.cost

  def random_solve(self, seed : int = 0) -> Solve:
    random.seed(seed)
    tour = list(range(1,self.size+1))
    random.shuffle(tour)
    solve = Solve(self.size, tour)
    return solve

    