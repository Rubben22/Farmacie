import click

@click.command()
def auth():
    username = click.prompt('username_mesaj')
    password = click.prompt('password', hide_input=True, confirmation_prompt=True, prompt_suffix='>')

    click.echo(f"login {username}")