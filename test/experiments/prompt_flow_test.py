import unittest
from unittest.mock import MagicMock, mock_open, patch

import pytest
from src.experiments.prompt_flow import PromptFlowExperiment


class TestPromptFlowExperiment:
    @patch('src.experiments.prompt_flow.PromptFlowExperiment._run_command')
    def test_create_resources(self, mock_run_command):
        experiment = PromptFlowExperiment("test-experiment")    
        mock_run_command.return_value = 0

        experiment.create_resources()

        expected_command = f'pf flow init --flow "./app/flow/{experiment.name}" --type standard'
        mock_run_command.assert_called_once_with(expected_command)

    @patch('shutil.copyfile')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="This is a template for {{name}}")
    def test_create_documentation(self, mock_open, mock_copyfile):  # noqa: F811
        experiment = PromptFlowExperiment("test-experiment")    
        experiment.create_documentation()

        mock_copyfile.assert_called_once_with('./src/artefacts/TEMPLATE-README.md', f"./app/flow/{experiment.name}/README.md")

        mock_open.assert_called_with(f"./app/flow/{experiment.name}/README.md", 'w')
        handle = mock_open()
        handle.write.assert_called_once_with('This is a template for test-experiment')

    @patch('subprocess.Popen')
    def test_run_command_failure(self, mock_popen):
        experiment = PromptFlowExperiment("test-experiment")    
        mock_process = MagicMock()
        mock_process.communicate.return_value = (b'', b'')
        mock_process.returncode = 1
        mock_popen.return_value = mock_process

        command = 'echo hello'
        with pytest.raises(RuntimeError, match=f'Error executing command: {command}'):
            experiment._run_command(command)
