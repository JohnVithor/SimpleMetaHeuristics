import copy

class Solve:
  """
  Solve é uma Solução para uma instância do Problema do Caixeiro Viajante (Problem)
  
  Esta classe além de encapsular o vetor com o percurso-solução de uma instância
  do problema, armazena o custo da solução e implementa algumas funções 
  utilitárias para auxiliar na manipulação dessas soluções.

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
  def __init__(self, size:int, tour = None):
    """
    Construtor de uma Solução (Solve)
    Precisa obrigatoriamente que seja informado um tamanho para a solução, o 
    tamanho do percurso-solução e opcionalmente o percurso em si

    :parâmetro size: int
    :parâmetro size: list[int] = None
    """
    self.size : int = size
    self.cost : float = -1
    self.tour : list(int) = [0] * self.size
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

  def circular_equal(self, other) -> bool:
    if self.size != other.size:
      return False

    self_str = ' '.join(map(str, self.tour))
    other_str = ' '.join(map(str, other.tour))
    
    if len(self_str) != len(other_str):
      return False

    return self_str in other_str + ' ' + other_str

  def __hash__(self):
    return hash((self.size, tuple(self.tour)))

    