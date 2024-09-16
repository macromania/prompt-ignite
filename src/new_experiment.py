import os
import re
import shutil
import subprocess


class NewExperiment:
    """Creates a new experiment.

    This class provides methods to run a command, check and connect to a virtual environment,
    read and set environment variables, create a Prompt Flow connection, create an experiment documentation,
    get the experiment name, check and create the flow directory, and create an experiment flow. 

    TODO: Seperate concerns into different classes
    """

    def _run_command(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode != 0:
            raise RuntimeError(f'Error executing command: {command}')
        return process.returncode

    def _check_and_connect_virtual_env(self):
        print("🔍 Checking if the virtual environment is active...")
        if 'VIRTUAL_ENV' not in os.environ:
            print("Not in a virtual environment. Connecting to it...")
            self._run_command('source .venv/bin/activate')

            print("✅ Connected to the virtual environment!")
        else:
            print(
                f"✅ Already connected to a virtual environment: {os.environ['VIRTUAL_ENV']}")

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
            lines = file.readlines()
            for line in lines:
                if not line.startswith('#'):
                    varname, value = line.strip().split('=')
                    print(f"🛠️ Setting {varname} as environment variable")
                    os.environ[varname] = value

    def _create_prompt_flow_connection(self, name):
        print("🛠️ Creating the Prompt Flow Connection...")
        self._run_command(
            f'pf connection create -f ./src/connections/azure_openai.yaml --set api_key="$AZURE_OPENAPI_KEY" api_base="$AZURE_OPENAPI_ENDPOINT" api_version="$AZURE_OPENAPI_VERSION" --name {name}-connection')

        print("✅ Connection created!")

    def _create_experiment_doc(self, name):
        print("🛠️ Creating experiment doc")

        shutil.copyfile('./src/artefacts/TEMPLATE-README.md',
                        f"./app/flow/{name}/README.md")

        with open(f"./app/flow/{name}/README.md") as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('{{name}}', name)

        # Write the file out again
        with open(f"./app/flow/{name}/README.md", 'w') as file:
            file.write(filedata)

        print("✅ Experiment doc created!")

    def _get_experiment_name(self):
        name = input("🤖 Enter the name of the experiment: ")
        while not re.match(r'^issue-[0-9]+-[a-z0-9-]+$', name):
            print(
                "Invalid name. The name should be in the format 'issue-{number}-{name}', i.e. issue-123-name, issue-456-name-123")
            name = input("🤖 Enter the name of the experiment: ")
        return name

    def _check_and_create_flow_directory(self):
        # TODO: Ask if the user where to create the flow directory
        print("🔍 Checking if the app/flow directory exists, creating if missing...")
        os.makedirs('./app/flow', exist_ok=True)

    def _create_experiment_flow(self, name):
        # TODO: Ask which template to create the experiment from
        print("🛠️ Creating the experiment flow...")
        self._run_command(
            f'pf flow init --flow "./app/flow/{name}" --type standard')

    def create(self):
        print("🔥 Welcome to the Prompt Ignite!")

        self._check_and_connect_virtual_env()
        self._read_and_set_env_vars()

        name = self._get_experiment_name()

        self._create_prompt_flow_connection(name)
        self._check_and_create_flow_directory()
        self._create_experiment_flow(name)
        self._create_experiment_doc(name)

        print("🔥 Experiment setup complete! 🚀")


if __name__ == "__main__":
    NewExperiment().create()
