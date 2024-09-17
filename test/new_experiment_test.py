import os
import subprocess
import pytest
import unittest
from unittest.mock import patch, MagicMock
from src.experiment_manager import NewExperiment

class TestNewExperiment:
    @pytest.fixture
    def new_experiment(self):
        return NewExperiment()

    @patch('subprocess.Popen')
    def test_run_command(self, mock_popen, new_experiment):
        mock_process = MagicMock()
        mock_process.wait.return_value = None
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        command = 'echo hello'
        return_code = new_experiment._run_command(command)

        mock_popen.assert_called_once_with(command, shell=True, stdout=subprocess.PIPE)
        assert return_code == 0

    @patch('os.environ', {})
    @patch('src.new_experiment.NewExperiment._run_command')
    def test_check_and_connect_virtual_env_not_connected(self, mock_run_command, new_experiment):
        new_experiment._check_and_connect_virtual_env()
        mock_run_command.assert_called_once_with('source .venv/bin/activate')

    @patch('os.environ', {'VIRTUAL_ENV': '/path/to/venv'})
    def test_check_and_connect_virtual_env_connected(self, new_experiment):
        new_experiment._check_and_connect_virtual_env()

    @patch('os.path.exists')
    @patch('os.environ', {})
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="VARNAME=value")
    def test_read_and_set_env_vars(self, mock_open, mock_exists, new_experiment):
        mock_exists.return_value = True
        new_experiment._read_and_set_env_vars()
        assert os.environ['VARNAME'] == 'value'