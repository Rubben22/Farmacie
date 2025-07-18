import click


@click.command()
@click.argument('nume')
@click.option('--lang',
              help='specify a language code',
              default='en')
def greet(nume, lang):
    """display greeting to user"""
    if lang == 'en':
        greetings = 'Hello '
    elif lang == 'es':
        greetings = 'Hola '
    else:
        raise click.BadOptionUsage('lang', 'Unsupported language')
    click.echo(f"{greetings}{nume}")

#we can change all the code into a simpler form
@click.command()
@click.argument('nume')
@click.option('--lang',
              help='specify a language code',
              default='en',
              type=click.Choice(['en', 'es', 'fr']))
@click.option('--say-it',
              help='How many times to display',
              default=1,
              type=int)
def greet1(nume, lang, say_it):
    """display greeting to user"""
    greetings = 'Hello ' if lang == 'en' else 'Holla ' if lang == 'es' else 'Bonjour'
    for i in range(say_it):
        click.echo(f"{greetings}{nume}")