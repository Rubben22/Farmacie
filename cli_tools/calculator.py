import click

@click.command()
@click.argument('xs', type=int, nargs=-1)
def add(xs):
    """sum of n numbers"""
    click.echo(sum(xs))

@click.command()
@click.argument('x', type=int)
@click.argument('y', type=int)
def substract(x, y):
    """add two numbers"""
    click.echo(f"diff= {x-y}")