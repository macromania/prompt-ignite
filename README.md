# Prompt Ignite Framework

## Overview

This framework facilitates the creation of experiments leveraging [Prompt Flow](https://github.com/microsoft/promptflow), Python, and Jupyter Notebooks. It is designed to streamline the process of testing hypotheses and analyzing results for engineers and data scientists in the field of AI.

## Features

- **Issue Tracking**: Each experiment is assigned a unique issue number for easy tracking and reference.
- **Template Types**: Every experiment can be initiated with one of three templates:
  1. ✅ Prompt flow with a simple prompt for Large Language Models (LLM).
  2. **[TODO]** Prompt flow with a simple Python tool.
  3. **[TODO]** Prompt flow with pre-processing in Python, prompt with LLM, and post-processing with Python.
  4. **[TODO]** Jupyter Notebook for data exploration and analysis.
  5. **[TODO]** Pure Python for simple Python tools.
  6. **[TODO]** Prompty with a simple LLM command.
- **Experiment Artifact**: Includes a `README.md` for detailing hypotheses, findings, and prompts used during the experiment.
- **Variants and Runners**: Each experiment comes with 2 variants and its runners, along with a runner notebook to facilitate different testing scenarios.

## Getting Started

Start a new experiment by running the following command:

```bash
make new-experiment
```

This command will prompt you to enter the name of the experiment and issue number. It will then create a new folder with the experiment structure.
Default values are provided for the issue number and experiment name, but you can change them as needed. You can also set the directory where the experiment will be created.

> **Currently only `prompt-flow` option is available for the experiment template type. Other template types will be added in the future.**

Following example shows how to create a new experiment:

```bash
🔥 Welcome to the Prompt Ignite!
Experiment Name [experiment]: demo
Issue Number [166381]: 42
Experiment Type: prompt-flow, jupyter, prompty, pure-python [prompt-flow]: prompt-flow
Directory to store the experiment artefacts [app/experiments]: 
Creating experiment: issue-42-demo for type: prompt-flow in directory: app/experiments
Confirm creating the experiment? [y/N]: y
Working...
🛠️ Creating the Prompt Flow...
✅ Prompt Flow created!
🛠️ Creating experiment doc
✅ Experiment doc created!
🔥 Experiment setup complete! 🚀
Done!
```

This is what the experiment structure looks like for `prompt-flow` using above example:

```bash
.
└── experiments
    └── issue-42-demo
        ├── README.md
        ├── data.jsonl
        ├── flow.dag.yaml
        ├── hello.jinja2
        ├── hello.py
        └── requirements.txt
```

### Local Development

Opening the project using `devcontainer` in Visual Studio Code is recommended for local development. This will provide you with a consistent development environment and all the necessary tools to work on the project.

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit <https://cla.opensource.microsoft.com>.

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
