import typer


def main(name: str = "", type: str = "", dir: str = ""):
    """_summary_

    Args:

        name (str, optional): _description_. Defaults to "".

        type (str, optional): _description_. Defaults to "".

        dir (str, optional): _description_. Defaults to "".

    """
    print(f"Creating experiment: {name} for type: {type} in directory: {dir}")


if __name__ == "__main__":
    typer.run(main)
