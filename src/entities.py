from abc import ABC, abstractmethod
from enum import Enum


class Experiment(ABC):
    def __init__(self, name, dir):
        self.name = name
        self.dir = dir

    @abstractmethod
    def create(self):
        pass


class ExperimentType(Enum):
    PROMPT_FLOW = "prompt-flow"
    JUPYTER_NOTEBOOK = "jupyter"
    PROMPTY = "prompty"
    PYTHON = "pure-python"
