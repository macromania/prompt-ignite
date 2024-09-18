from abc import ABC, abstractmethod
from enum import Enum


class ExperimentType(Enum):
    PROMPT_FLOW = 'Hello Prompt Flow'
    JUPYTER_NOTEBOOK = 'Hello Jupyter Notebook'
    PROMPTY = 'Hello Prompty'
    PYTHON = 'Hello Python'


class Experiment(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def create(self):
        pass
