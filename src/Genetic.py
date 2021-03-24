from Problem import Problem
from Solve import Solve
import random
import time
from typing import Callable
class Genetic:
  """
  """

  def mutate_side(solve:Solve) -> Solve:
    rate:float = 1.0 / solve.size
    for i in range(solve.size):
      if random.random() < rate:
        side = 1 if random.random() < 0.5 else -1
        aux = solve.tour[i]
        pos = (i+side) % solve.size
        solve.tour[i] = solve.tour[pos]
        solve.tour[pos] = aux
    return solve

  def mutate_rand(solve:Solve) -> Solve:
    rate:float = 1.0 / solve.size
    for i in range(solve.size):
      if random.random() < rate:
        aux = solve.tour[i]
        pos:int = random.randint(0, solve.size-1)
        solve.tour[i] = solve.tour[pos]
        solve.tour[pos] = aux
    return solve

  def cross_over(parent_a:Solve, parent_b:Solve, child:Solve) -> Solve:
    pos:int = random.randint(0, child.size-1)
    child.tour[:pos] = parent_a.tour[:pos]
    child.tour[pos:] = [item for item in parent_b.tour if item not in child.tour[:pos]]
    return child

  def cross_over_frag(parent_a:Solve, parent_b:Solve, child:Solve) -> Solve:
    start_pos:int = random.randint(0, child.size-1)
    end_pos:int = random.randint(0, child.size-1)
    if(start_pos > end_pos):
      start_pos, end_pos = end_pos, start_pos
    child.tour[:end_pos-start_pos] = parent_a.tour[start_pos:end_pos]
    child.tour[end_pos-start_pos:] = [item for item in parent_b.tour if item not in parent_a.tour[start_pos:end_pos]]
    return child

  def __init__(self, problem:Problem, seed:int=0, mutation_method:Callable = mutate_rand, cross_over_method:Callable = cross_over_frag):
    self.problem:Problem = problem
    self.original_seed:int = seed
    self.mutation_method = mutation_method
    self.cross_over_method = cross_over_method

  def run(self, contest_size:int=2, cross_rate:float=0.8, mutate_rate:float=0.1, size:int=30, epochs:int=20, max_time:float=60.0, start_solve:Solve = None) -> Solve:
    random.seed(self.original_seed)
    if start_solve is not None:
      self.best_solve = start_solve.copy()
    else:
      self.best_solve : Solve = self.generate_random_solve(size*epochs)
    
    population : list(Solve) = [self.generate_random_solve(size*epochs) for i in range(size-1)]
    population.append(self.best_solve)

    step = 0
    initial_time = time.time()
    end_time = time.time()
    
    while step < epochs and (end_time - initial_time) <= max_time:
      new_population:list(Solve) = []
      for parent in population:
        other_parent:Solve = self.select_parent(population, contest_size)
        
        child_a:Solve = parent.copy()
        child_b:Solve = other_parent.copy()

        if random.random() < cross_rate:
          child_a = self.cross_over_method(parent, other_parent, child_a)
          child_b = self.cross_over_method(other_parent, parent, child_b)
        if random.random() < mutate_rate:
          child_a = self.mutation_method(child_a)
          child_b = self.mutation_method(child_b)

        new_population.append(child_a)
        new_population.append(child_b)

        self.compare_with_best(child_a)
        self.compare_with_best(child_b)

      ordered_new_population = sorted(new_population, key=lambda x: x.cost)
      population = ordered_new_population[:size]
      step += 1
      end_time = time.time()
    return self.best_solve, step

  def generate_random_solve(self, interval:int=100) -> Solve:
    p_seed = random.randint(-(interval),(interval))
    old_state = random.getstate()
    solve : Solve = self.problem.random_solve(p_seed)
    random.setstate(old_state)
    self.compare_with_best(solve)
    return solve
  
  def compare_with_best(self, solve:Solve) -> Solve:
    if self.problem.evaluate(solve) < self.problem.evaluate(self.best_solve):
      self.best_solve = solve.copy()
    return self.best_solve

  def select_parent(self, population:list, contest_size:int) -> Solve:
    best_candidate:Solve = population[random.randint(0, len(population)-1)]
    for i in range(contest_size-1):
      solve:Solve = population[random.randint(0, len(population)-1)]
      if self.problem.evaluate(solve) < self.problem.evaluate(best_candidate):
        best_candidate = solve
    return best_candidate


