from src.experiments.base_experiment import Experiment


class JupyterNotebookExperiment(Experiment):
    def create(self):
        raise NotImplementedError("Jupyter Notebook experiment not implemented yet.")
