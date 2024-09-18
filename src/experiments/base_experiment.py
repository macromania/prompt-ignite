from abc import ABC, abstractmethod


class Experiment(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def create(self):
        pass
