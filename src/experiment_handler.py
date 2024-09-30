import os
import re
import subprocess

from config import DEFAULT_EXPERIMENT_DIR
from src.entities import ExperimentType
from src.experiments.jupytor_notebook import JupyterNotebookExperiment
from src.experiments.prompt_flow import PromptFlowExperiment
from src.experiments.prompty import PromptyExperiment
from src.experiments.pure_python import PythonExperiment


class ExperimentHandler:
    _experiments = {
        ExperimentType.PROMPT_FLOW: PromptFlowExperiment,
        ExperimentType.JUPYTER_NOTEBOOK: JupyterNotebookExperiment,
        ExperimentType.PROMPTY: PromptyExperiment,
        ExperimentType.PYTHON: PythonExperiment,
    }

    def __init__(self):
        self._check_and_connect_virtual_env()
        self._read_and_set_env_vars()

    def _check_and_connect_virtual_env(self):
        print("🔍 Checking if the virtual environment is active...")
        if "VIRTUAL_ENV" not in os.environ:
            print("Not in a virtual environment. Connecting to it...")
            self._run_command("source .venv/bin/activate")

            print("✅ Connected to the virtual environment!")
        else:
            print(
                f"✅ Already connected to a virtual environment: {os.environ['VIRTUAL_ENV']}")

    def _read_and_set_env_vars(self):
        print("🔍 Reading .env file...")

        if not os.path.exists(".env"):
            print("""
            No .env file found. Please create a .env file in the root directory of the project.
            The .env file should contain the following variables:
            AZURE_OPENAPI_KEY=<your-azure-openapi-key>
            AZURE_OPENAPI_ENDPOINT=<your-azure-openapi-endpoint>
            AZURE_OPENAPI_VERSION=<your-azure-openapi-version>
            """)
            return

        with open(".env") as file:
            for line in file:
                if not line.strip() or line.startswith("#"):
                    continue
                try:
                    varname, value = line.strip().split("=", 1)
                    os.environ[varname] = value
                except ValueError:
                    print(f"Error parsing line: {line.strip()}")

    def _run_command(self, command):
        env = os.environ.copy()
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        stdout, stderr = process.communicate(timeout=30)
        if process.returncode != 0:
            raise RuntimeError(
                f"Error executing experiment command: {command}")
        return process.returncode

    @staticmethod
    def _get_experiment_name():
        name = input("🤖 Enter the name of the experiment: ")
        while not re.match(r"^issue-[0-9]+-[a-z0-9-]+$", name):
            print(
                "🚨 Invalid name. The name should be in the format 'issue-{number}-{name}', i.e. issue-123-name, issue-456-name-123")
            name = input("🤖 Enter the name of the experiment: ")
        return name

    @staticmethod
    def _get_experiment_type():
        """Prompts the user to choose a type for the experiment."""
        types = {"1": ExperimentType.PROMPT_FLOW, "2": ExperimentType.JUPYTER_NOTEBOOK,
                 "3": ExperimentType.PROMPTY, "4": ExperimentType.PYTHON}

        print("🔍 Choose a type for the experiment:")
        for key, value in types.items():
            print(f"{key}. {value.value}")

        choice = input("🔢 Enter the number of your choice: ")
        while choice not in types:
            print(
                "🚨 Invalid choice. Please enter a number corresponding to one of the options.")
            choice = input("🔢 Enter the number of your choice: ")

        return types[choice]

    @staticmethod
    def _get_experiment_dir():
        """Prompt the user to provide a custom directory or use the default."""
        user_input = input(
            f"📁 [Optional] Enter directory for experiment (default: {DEFAULT_EXPERIMENT_DIR}) : ").strip()

        # Use default if no input
        if not user_input:
            chosen_directory = DEFAULT_EXPERIMENT_DIR
            print(f" ℹ️ Using default directory: {chosen_directory}")
        else:
            chosen_directory = user_input

            # If the input does not start with './', prepend it
            if not os.path.isabs(chosen_directory) and not chosen_directory.startswith('./'):
                chosen_directory = f"./{chosen_directory}"

            # Automatically append '/' if it doesn't end with '/'
            if not chosen_directory.endswith('/'):
                chosen_directory = f"{chosen_directory}/"

            print(f" ℹ️ Using custom directory: {chosen_directory}")

        # Create if does not exist
        if not os.path.exists(chosen_directory):
            os.makedirs(chosen_directory)
            print(f"📁 Created directory: {chosen_directory}")
        else:
            print(f"📁 Directory already exists: {chosen_directory}")

        return chosen_directory

    @classmethod
    def create(cls, name: str, type: ExperimentType, dir: str):
        try:
            experiment = cls._experiments[type](name, dir)
            experiment.create()

            print("🔥 Experiment setup complete! 🚀")

        except NotImplementedError:
            print("🛠️ This setup is not implemented yet!")
            return
        except Exception as e:
            print(f"❌ Oops! Something went wrong. {e}")
            return


# if __name__ == "__main__":
#     ExperimentHandler.create()
