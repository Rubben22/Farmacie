import typing

import click

@click.command()
@click.argument('fr', type=click.File('r'))
def note(fo: typing.TextIO):
    """Read from a file"""
    #click.echo("Enter the text")
    try:
        while True:
            value = click.prompt('',prompt_suffix='>')
            fo.write(f"{value}\n")
    except click.Abort:
        click.echo("Abort")