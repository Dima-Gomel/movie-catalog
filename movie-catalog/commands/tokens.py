from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens

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
):
    """
    Check if the passed token is valid - exists or not.
    """
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[bold green]exists.[/bold green]"
            if redis_tokens.token_exists(token)
            else "[bold red]doesn't exist.[/bold red]"
        ),
    )
    print(token)


@app.command(name="list")
def list_tokens():
    """
    List all tokens.
    """
    print(Markdown("# Availabl API Tokens"))
    print(Markdown("\n-".join([""] + redis_tokens.get_tokens())))
    print()


@app.command(name="add")
def add_token(token: Annotated[str, str]):
    """
    Create a new token.
    """
    print(Markdown("# Add API Tokens"))
    redis_tokens.add_token(token)
    print(Markdown(f"## Token add: `{token}`"))
    print(Markdown("**Save this token securely!**"))


@app.command(name="create")
def create_token():
    """
    Create a new token.
    """
    print(Markdown("# Create API Tokens"))
    tokens = redis_tokens.generate_token()
    print(Markdown(f"# Token create: `{tokens}`"))
    redis_tokens.add_token(tokens)
    print(Markdown(f"Save token: `{tokens}`"))


@app.command(name="rm")
def delete_token(token: Annotated[str, str]):
    """
    Remove a token.
    """
    print(Markdown("# Remove API Tokens"))
    redis_tokens.delete_token(token)
    print(Markdown(f"## Token remove: `{token}`"))
