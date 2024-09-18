import os
import shutil
import subprocess

from src.experiments.base_experiment import Experiment


class PromptFlowExperiment(Experiment):
    def create(self):
        self.create_resources()
        self.create_documentation()

    def create_resources(self):
        print("🛠️ Creating the Prompt Flow...")
        command = f'pf flow init --flow "./app/flow/{self.name}" --type standard'
        self._run_command(command)
        print("✅ Prompt Flow created!")

    def create_documentation(self):
        print("🛠️ Creating experiment doc")

        shutil.copyfile('./src/artefacts/TEMPLATE-README.md', f"./app/flow/{self.name}/README.md")

        with open(f"./app/flow/{self.name}/README.md") as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('{{name}}', self.name)

        # Write the file out again
        with open(f"./app/flow/{self.name}/README.md", 'w') as file:
            file.write(filedata)

        print("✅ Experiment doc created!")

    def _run_command(self, command):
        env = os.environ.copy()
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        stdout, stderr = process.communicate(timeout=30)
        if process.returncode != 0:
            raise RuntimeError(f'Error executing command: {command}')
        return process.returncode
