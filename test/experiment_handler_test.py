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

    @patch('src.experiments.prompt_flow.PromptFlowExperiment.create_documentation')
    @patch('src.experiments.prompt_flow.PromptFlowExperiment.create_resources')
    def test_create(self, mock_create_documentation, mock_create_resources):
        experiment = PromptFlowExperiment("test-experiment")
        dir = "./mydir/"

        experiment.create(dir)
        
        mock_create_resources.assert_called_once_with(dir)
        mock_create_documentation.assert_called_once_with(dir)

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

    @patch.object(ExperimentHandler, '_check_and_connect_virtual_env')
    @patch.object(ExperimentHandler, '_read_and_set_env_vars')
    @patch('builtins.input', return_value='')
    @patch('os.path.exists', return_value=False) 
    @patch('os.makedirs')
    def test_get_experiment_dir_default(self, mock_makedirs, mock_exists, mock_input, mock_read_and_set_env_vars, mock_check_and_connect_virtual_env):
        experiment = ExperimentHandler()
        
        result = experiment._get_experiment_dir()
        
        expected_directory = "./app/flow/"
        mock_makedirs.assert_called_once_with(expected_directory)
        assert result == expected_directory

    @patch.object(ExperimentHandler, '_run_command')
    @patch('builtins.input', return_value='mydir')  # Simulate user input without './' and without '/'
    @patch('os.path.exists', return_value=False)  # Simulate directory does not exist
    @patch('os.makedirs')
    def test_get_experiment_dir_custom_relative(self, mock_makedirs, mock_exists, mock_input, mock_run_command):
        experiment = ExperimentHandler()

        
        result = experiment._get_experiment_dir()
        
        expected_directory = "./mydir/"
        mock_makedirs.assert_called_once_with(expected_directory)
        assert result == expected_directory

    @patch.object(ExperimentHandler, '_run_command')
    @patch('builtins.input', return_value='./mydir')  # Simulate user input with './' but without '/'
    @patch('os.path.exists', return_value=False)  # Simulate directory does not exist
    @patch('os.makedirs')
    def test_get_experiment_dir_custom_relative_with_dot_slash(self, mock_makedirs, mock_exists, mock_input, mock_run_command):
        experiment = ExperimentHandler()

        
        result = experiment._get_experiment_dir()
        
        expected_directory = "./mydir/"
        mock_makedirs.assert_called_once_with(expected_directory)
        assert result == expected_directory

    @patch.object(ExperimentHandler, '_run_command')
    @patch('builtins.input', return_value='/absolute/path')  # Simulate absolute path input
    @patch('os.path.exists', return_value=False)  # Simulate directory does not exist
    @patch('os.makedirs')
    def test_get_experiment_dir_absolute(self, mock_makedirs, mock_exists, mock_input, mock_run_command):
        experiment = ExperimentHandler()

        
        result = experiment._get_experiment_dir()
        
        expected_directory = "/absolute/path/"
        mock_makedirs.assert_called_once_with(expected_directory)
        assert result == expected_directory

    @patch.object(ExperimentHandler, '_read_and_set_env_vars')
    @patch.object(ExperimentHandler, '_run_command')
    @patch('builtins.input', return_value='./existingdir')  # Simulate existing directory
    @patch('os.path.exists', return_value=True)  # Simulate directory already exists
    def test_get_experiment_dir_existing_directory(self, mock_exists, mock_input, mock_run_command, mock_read_and_set_env_vars):
        experiment = ExperimentHandler()

        
        result = experiment._get_experiment_dir()
        
        expected_directory = "./existingdir/"
        mock_exists.assert_called_once_with(expected_directory)
        assert result == expected_directory
