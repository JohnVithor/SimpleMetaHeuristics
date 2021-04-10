import abc
from Solve import Solve
from Problem import Problem

class AlgorithmInterface(metaclass=abc.ABCMeta):

    def __init__(self, problem:Problem, seed:int):
        self.problem:Problem = problem
        self.seed:int = seed

    @abc.abstractmethod
    def run(self, parameters:dict) -> Solve:
        return
    
    @abc.abstractmethod
    def copy(self):
        return

