import copy

class Solve:
  def __init__(self, size:int, tour = None):
    self.size : int = size
    self.cost : int = -1
    self.tour : [0]*self.size
    if tour != None:
      if len(tour) != self.size:
        raise NameError(f'Tour of a different size!: Expected size = {self.size} and actual size = {len(tour)}') 
      self.tour : list = tour.copy()

  def __copy__(self):
    return self.copy()

  def copy(self):
    return Solve(copy.copy(self.size), copy.copy(self.tour))

  def __deepcopy__(self, memo : dict = {}):
    return self.deepcopy()

  def deepcopy(self, memo : dict = {}):
    return Solve(copy.deepcopy(self.size), copy.deepcopy(self.tour))

  def __str__(self):
    return f'Solve of tour {self.tour}'

  def __repr__(self):
    return f'{self.tour}'

  def __eq__(self, other):
    return self.size == other.size and tuple(self.tour) == tuple(other.tour)

  def circular_equal(self, other):
    if self.size != other.size:
      return False

    self_str = ' '.join(map(str, self.tour))
    other_str = ' '.join(map(str, other.tour))
    
    if len(self_str) != len(other_str):
      return False

    return self_str in other_str + ' ' + other_str

  def __hash__(self):
    return hash((self.size, tuple(self.tour)))

    