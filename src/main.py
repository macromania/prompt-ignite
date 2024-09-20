import time
from typing import Annotated

import typer

from src.entities import ExperimentType


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

name_help = f"Name of the experiment (default: {d_name})"
issue_help = "Issue number (default: auto-generated)"
type_help = f"Type of the experiment. (default: {d_type})"
dir_help = f"Directory to store the experiment (default: {d_dir})"


def main(name: Annotated[str | None, typer.Option(help=name_help, show_default=False)] = None,  # noqa: 501
         issue: Annotated[int | None, typer.Option(help=issue_help, show_default=False)] = None,  # noqa: 501
         type: Annotated[ExperimentType | None, typer.Option(help=type_help, show_default=False)] = None,  # noqa: 501
         dir: Annotated[str | None, typer.Option(help=dir_help, show_default=False)] = None):  # noqa: 501
    """
    🔥 Welcome to the Prompt Ignite!
    """

    if not name:
        name = typer.prompt(
            "Enter the name of the experiment:",
            default=d_name)

    if not issue:
        issue = typer.prompt("Enter issue number:",
                             default=d_issue,
                             type=int)

    if not type:
        type = typer.prompt(
            f"Enter the type of the experiment, Choose from: {', '.join([t.value for t in ExperimentType])}",
            default=d_type,
            type=ExperimentType,
            show_choices=True)

    if not dir:
        dir = typer.prompt(
            "Enter the directory to store the experiment:",
            default=d_dir)
    print(
        f"Creating experiment: issue-{issue}-{name} for type: {type.value} in directory: {dir}")


if __name__ == "__main__":
    typer.run(main)
