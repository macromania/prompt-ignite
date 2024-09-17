import os
import re
import subprocess

from src.experiment import ExperimentType
from src.prompt_flow_experiment import PromptFlowExperiment


class ExperimentFactory:
    @staticmethod
    def create_experiment(experiment_type, name):
        if experiment_type == ExperimentType.PROMPT_FLOW:
            return PromptFlowExperiment(name)
        elif experiment_type == ExperimentType.JUPYTER_NOTEBOOK:
            raise NotImplementedError("Jupyter Notebook experiment not implemented yet.")
        elif experiment_type == ExperimentType.PROMPTY:
            raise NotImplementedError("Prompty experiment not implemented yet.")
        elif experiment_type == ExperimentType.PYTHON:
            raise NotImplementedError("Python experiment not implemented yet.")
        else:
            raise ValueError(f"Unsupported experiment type: {experiment_type}")


class ExperimentManager:
    def __init__(self):
        self._check_and_connect_virtual_env()
        self._read_and_set_env_vars()

    def _check_and_connect_virtual_env(self):
        print("🔍 Checking if the virtual environment is active...")
        if 'VIRTUAL_ENV' not in os.environ:
            print("Not in a virtual environment. Connecting to it...")
            self._run_command('source .venv/bin/activate')

            print("✅ Connected to the virtual environment!")
        else:
            print(f"✅ Already connected to a virtual environment: {os.environ['VIRTUAL_ENV']}")

    def _read_and_set_env_vars(self):
        print("🔍 Reading .env file...")

        if not os.path.exists('.env'):
            print("""
            No .env file found. Please create a .env file in the root directory of the project.
            The .env file should contain the following variables:
            AZURE_OPENAPI_KEY=<your-azure-openapi-key>
            AZURE_OPENAPI_ENDPOINT=<your-azure-openapi-endpoint>
            AZURE_OPENAPI_VERSION=<your-azure-openapi-version>
            """)
            return

        with open('.env') as file:
            for line in file:
                if not line.strip() or line.startswith('#'):
                    continue
                try:
                    varname, value = line.strip().split('=', 1)
                    os.environ[varname] = value
                    print(f"🛠️ Set environment variable: {varname}")
                except ValueError:
                    print(f"Error parsing line: {line.strip()}")

    def _run_command(self, command):
        env = os.environ.copy()
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise RuntimeError(f'Error executing experiment command: {command}')
        return process.returncode

    def _get_experiment_name(self):
        name = input("🤖 Enter the name of the experiment: ")
        while not re.match(r'^issue-[0-9]+-[a-z0-9-]+$', name):
            print(
                "Invalid name. The name should be in the format 'issue-{number}-{name}', i.e. issue-123-name, issue-456-name-123")
            name = input("🤖 Enter the name of the experiment: ")
        return name

    def _get_experiment_type(self):
        """Prompts the user to choose a type for the experiment."""
        types = {
            '1': ExperimentType.PROMPT_FLOW,
            '2': ExperimentType.JUPYTER_NOTEBOOK,
            '3': ExperimentType.PROMPTY,
            '4': ExperimentType.PYTHON
        }

        print("🔍 Choose a type for the experiment:")
        for key, value in types.items():
            print(f"{key}. {value.value}")

        choice = input("Enter the number of your choice: ")
        while choice not in types:
            print("Invalid choice. Please enter a number corresponding to one of the options.")
            choice = input("Enter the number of your choice: ")

        return types[choice]

    def create(self):
        try:
            print("🔥 Welcome to the Prompt Ignite!")

            name = self._get_experiment_name()
            experiment_type = self._get_experiment_type()

            experiment = ExperimentFactory.create_experiment(experiment_type, name)
            experiment.create_resources()
            experiment.create_documentation()
            print("🔥 Experiment setup complete! 🚀")

        except NotImplementedError:
            print("🛠️ This setup is not implemented yet!")
            return
        except Exception as e:
            print(f"❌ Oops! Something went went wrong. {e}")
            return


if __name__ == "__main__":
    ExperimentManager().create()
