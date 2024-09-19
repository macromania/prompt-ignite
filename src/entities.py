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
    PROMPT_FLOW = "Hello Prompt Flow"
    JUPYTER_NOTEBOOK = "Hello Jupyter Notebook"
    PROMPTY = "Hello Prompty"
    PYTHON = "Hello Python"
