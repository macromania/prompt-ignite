import os
import subprocess
import unittest
from unittest.mock import MagicMock, patch

import pytest
from src.experiment_manager import ExperimentFactory, ExperimentManager, ExperimentType, PromptFlowExperiment


class TestExperimentFactory:
    @pytest.fixture
    def experiment_factory(self):
        return ExperimentFactory()

    def test_initiate_prompt_flow_experiment(self, experiment_factory):
        experiment = experiment_factory.initiate_experiment(ExperimentType.PROMPT_FLOW, 'issue-123-name')
        assert isinstance(experiment, PromptFlowExperiment)
    
    def test_initiate_jupyter_notebook_experiment(self, experiment_factory):
        with pytest.raises(NotImplementedError):
            experiment_factory.initiate_experiment(ExperimentType.JUPYTER_NOTEBOOK, 'issue-123-name')

    def test_initiate_prompty_experiment(self, experiment_factory):
        with pytest.raises(NotImplementedError):
            experiment_factory.initiate_experiment(ExperimentType.PROMPTY, 'issue-123-name')

    def test_initiate_python_experiment(self, experiment_factory):
        with pytest.raises(NotImplementedError):
            experiment_factory.initiate_experiment(ExperimentType.PYTHON, 'issue-123-name')


class TestExperimentManager:
    @pytest.fixture
    @patch.object(ExperimentManager, '_run_command')
    def experiment_manager(self, mock_run_command):
        mock_run_command.return_value = 0
        return ExperimentManager()

    @patch('subprocess.Popen')
    def test_run_command(self, mock_popen, experiment_manager):
        mock_process = MagicMock()
        # Simulate stdout and stderr
        mock_process.communicate.return_value = (b'', b'')
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        command = 'echo hello'
        return_code = experiment_manager._run_command(command)

        mock_popen.assert_called_once_with(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
        assert return_code == 0

    @patch('os.environ', {})
    @patch.object(ExperimentManager, '_run_command')
    def test_check_and_connect_virtual_env_not_connected(self, mock_run_command, experiment_manager):
        experiment_manager._check_and_connect_virtual_env()
        mock_run_command.assert_called_once_with('source .venv/bin/activate')

    @patch('os.environ', {'VIRTUAL_ENV': '/path/to/venv'})
    def test_check_and_connect_virtual_env_connected(self, experiment_manager):
        experiment_manager._check_and_connect_virtual_env()

    @patch('os.path.exists')
    @patch('os.environ', {})
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="VARNAME=value")
    def test_read_and_set_env_vars(self, mock_open, mock_exists, experiment_manager):
        mock_exists.return_value = True
        experiment_manager._read_and_set_env_vars()
        assert os.environ['VARNAME'] == 'value'
