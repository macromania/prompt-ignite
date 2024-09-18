import os
import subprocess
from unittest.mock import MagicMock, mock_open, patch

from src.experiment_handler import ExperimentHandler
from src.experiments.prompt_flow import PromptFlowExperiment


class TestExperimentHandler:
    @patch('src.experiment_handler.ExperimentHandler._run_command')
    @patch.dict(os.environ, {}, clear=True)
    def test_check_and_connect_virtual_env_not_connected(self, mock_run_command):
        ExperimentHandler()
        mock_run_command.assert_called_once_with('source .venv/bin/activate')

    @patch('os.environ', {'VIRTUAL_ENV': '/path/to/venv'})
    @patch('src.experiment_handler.ExperimentHandler._run_command')
    def test_check_and_connect_virtual_env_connected(self, mock_run_command):
        ExperimentHandler()
        mock_run_command.assert_not_called()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="VARNAME=value")
    @patch('src.experiment_handler.ExperimentHandler._run_command')
    def test_read_and_set_env_vars(self, mock_exists, mock_open, mock_run_command):
        mock_exists.return_value = True
        ExperimentHandler()
        mock_open.assert_called_once_with('.env')

    @patch.object(PromptFlowExperiment, '_run_command')
    @patch.object(PromptFlowExperiment, 'create_documentation')
    def test_create(self, mock_create_documentation, mock_run_command):
        experiment = PromptFlowExperiment("test-experiment")
        
        experiment.create()

        mock_run_command.assert_called_once_with('pf flow init --flow "./app/flow/test-experiment" --type standard')
        mock_create_documentation.assert_called_once()

    @patch('subprocess.Popen')
    @patch('os.environ', {'VIRTUAL_ENV': '/path/to/venv'})
    def test_run_command(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = (b'', b'')
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        command = 'echo hello'
        experiment_handler = ExperimentHandler()
        return_code = experiment_handler._run_command(command)

        mock_popen.assert_called_once_with(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
        assert return_code == 0
