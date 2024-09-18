from src.entities import Experiment


class JupyterNotebookExperiment(Experiment):
    def create(self):
        raise NotImplementedError("Jupyter Notebook experiment not implemented yet.")
