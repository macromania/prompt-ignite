import time
from typing import Annotated

import typer

from src.entities import ExperimentType
from src.experiment_handler import ExperimentHandler


def generate_random_int_from_timestamp():
    # Get the current timestamp in milliseconds
    timestamp = int(time.time() * 1000)

    # Use the timestamp to generate a random integer
    random_int = timestamp % 1000000  # Example: limit to 6 digits
    return random_int


d_name = "experiment"
d_type = ExperimentType.PROMPT_FLOW.value
d_issue = generate_random_int_from_timestamp()
d_dir = "app/experiments"

n_help = f"Name of the experiment (default: {d_name})"
i_help = "Issue number (default: auto-generated)"
t_help = f"Type of the experiment. (default: {d_type})"
d_help = f"Directory to store the experiment (default: {d_dir})"

n_typerOption = typer.Option(help=n_help, show_default=False)
i_typerOption = typer.Option(help=i_help, show_default=False)
t_typerOption = typer.Option(help=t_help, show_default=False)
d_typerOption = typer.Option(help=d_help, show_default=False)


def main(name: Annotated[str | None, n_typerOption] = None,
         issue: Annotated[int | None, i_typerOption] = None,
         type: Annotated[ExperimentType | None, t_typerOption] = None,
         dir: Annotated[str | None, d_typerOption] = None):
    """
    🔥 Welcome to the Prompt Ignite!
    """

    print("🔥 Welcome to the Prompt Ignite!")

    if not name:
        name = typer.prompt(
            "Experiment Name",
            default=d_name)

    if not issue:
        issue = typer.prompt("Issue Number",
                             default=d_issue,
                             type=int)

    if not type:
        type = typer.prompt(
            f"Experiment Type: {', '.join([t.value for t in ExperimentType])}",
            default=d_type,
            type=ExperimentType,
            show_choices=True)

    if not dir:
        dir = typer.prompt(
            "Directory to store the experiment artefacts",
            default=d_dir)

    conventional_name = f"issue-{issue}-{name}"

    summary = f"Creating experiment: {conventional_name} for type: {type.value} in directory: {dir}"
    print(summary)

    create = typer.confirm("Confirm creating the experiment?")
    if not create:
        print("Aborting...")
        raise typer.Abort()

    print("Working...")

    if type is None:
        raise ValueError("Experiment type is required")

    if dir is None:
        raise ValueError("Experiment directory is required")

    ExperimentHandler.create(name=conventional_name, type=type, dir=dir)

    print("Done!")


if __name__ == "__main__":
    typer.run(main)
