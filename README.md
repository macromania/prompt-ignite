# Prompt Ignite Framework

## Overview

This framework facilitates the creation of experiments leveraging [Prompt Flow](https://github.com/microsoft/promptflow), Python, and Jupyter Notebooks. It is designed to streamline the process of testing hypotheses and analyzing results for engineers and data scientists in the field of AI.

## Features

- **Issue Tracking**: Each experiment is assigned a unique issue number for easy tracking and reference.
- **Template Types**: Every experiment can be initiated with one of three templates:
  1. Prompt flow with a simple prompt for Large Language Models (LLM).
  2. Prompt flow with a simple Python tool.
  3. Prompt flow with pre-processing in Python, prompt with LLM, and post-processing with Python.
- **Experiment Artifact**: Includes a `README.md` for detailing hypotheses, findings, and prompts used during the experiment.
- **Variants and Runners**: Each experiment comes with 2 variants and its runners, along with a runner notebook to facilitate different testing scenarios.

## Getting Started

Work in progres...

## Experiment Structure

Each experiment folder is structured as follows:

- `issue-<issue_number>-<name>/`: The main directory for the experiment.
  - `README.md`: Details the experiment's hypothesis, findings, and prompts.
  - `flow.dag.yaml`: Contains the Prompt Flow flow.
  - `run.yaml`: Contains the default variant runner of the experiment.
  - `run-1.yaml`: Contains the first variant runner of the experiment.
  - `runner.ipynb`: The Jupyter Notebook for the second runner.
  - `data.jsonl`: The data file for the experiment.

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
