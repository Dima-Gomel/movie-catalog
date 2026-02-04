__all__ = ("app",)

from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens as tokens

app = typer.Typer(
    name="token",
    help="Tokens management.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(
            help="The token to check",
        ),
    ],
) -> None:
    """
    Check if the passed token is valid - exists or not.
    """
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[bold green]exists.[/bold green]"
            if tokens.token_exists(token)
            else "[bold red]doesn't exist.[/bold red]"
        ),
    )
    print(token)


@app.command(name="list")
def list_tokens() -> None:
    """
    List all tokens.
    """
    print(Markdown("# Availabl API Tokens"))
    print(Markdown("\n- ".join([""] + tokens.get_tokens())))
    print()


@app.command(name="add")
def add_token(
    token: Annotated[
        str,
        typer.Argument(
            help="The token to add.",
        ),
    ],
) -> None:
    """
    Add the provided token to db.
    """
    tokens.add_token(token)
    print(f"Token [bold]{token}[/bold] added to db.")


@app.command(name="create")
def create_token() -> None:
    """
    Create a new token.
    """
    new_token = tokens.generate_and_save_token()
    print(f"new token: [bold green]{new_token}[/bold green] save to db.")


@app.command(name="rm")
def delete_token(
    token: Annotated[
        str,
        typer.Argument(
            help="The token to delete.",
        ),
    ],
) -> None:
    """
    Delete the provided token from db.
    """
    if not tokens.token_exists(token):
        print(f"Token [bold]{token} [red]does not exist[/red][/bold].")
        return

    tokens.delete_token(token)
    print(f"Token [bold]{token}[/bold] removed from db.")
