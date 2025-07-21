import json
from datetime import date, datetime

import click
from pathlib import Path

from tabulate import tabulate
from pydantic import BaseModel


class Entitate(BaseModel):
    id_entitate: str


class Client(Entitate):
    nume: str
    prenume: str
    CNP: int
    data_nasterii: date

    def to_dict(self):
        return {
            "id_entitate": self.id_entitate,
            "nume": self.nume,
            "prenume": self.prenume,
            "CNP": self.CNP,
            "data_nasterii": self.data_nasterii.strftime("%d.%m.%Y")
        }


# ========= File Path ==========
CLIENT_FILE = Path.home() / "PycharmProjects/Farmacie/client.json"


def read_data():
    if CLIENT_FILE.exists():
        with open(CLIENT_FILE) as f:
            return json.load(f)
    return {}


def write_data(data):
    with open(CLIENT_FILE, 'w') as f:
        json.dump(data, f, indent=4)


# ========= CLI =========
@click.group()
@click.pass_context
def cli(ctx):
    """Client CLI group for CRUD operations"""
    ctx.ensure_object(dict)
    ctx.obj[ 'data' ] = read_data()


@cli.command()
@click.pass_context
def show(ctx):
    """Afișează toți clienții înregistrați"""
    data = ctx.obj[ 'data' ]
    if not data:
        click.echo("Nu există niciun client înregistrat.")
        return

    clients = [ ]
    for raw in data.values():
        raw.pop("py/object", None)
        client = Client(
            **{
                **raw,
                "data_nasterii": datetime.strptime(raw[ "data_nasterii" ], "%d.%m.%Y").date()
            }
        )
        clients.append([
            client.id_entitate,
            client.nume,
            client.prenume,
            client.CNP,
            client.data_nasterii.strftime("%d.%m.%Y")
        ])

    headers = [ "ID", "Nume", "Prenume", "CNP", "Data nașterii" ]
    click.echo(tabulate(clients, headers=headers, tablefmt="simple_outline"))


@cli.command()
@click.option('--id', prompt="ID", help="ID-ul clientului")
@click.option('--nume', prompt="Nume", help="Nume client")
@click.option('--prenume', prompt="Prenume", help="Prenume client")
@click.option('--cnp', prompt="CNP", type=int, help="CNP-ul clientului")
@click.option('--data-nasterii', prompt="Data nașterii (dd.mm.yyyy)", help="Data nașterii în format dd.mm.yyyy")
@click.pass_context
def add(ctx, id, nume, prenume, cnp, data_nasterii):
    """Adaugă un nou client"""
    data = ctx.obj[ 'data' ]

    if id in data:
        raise click.BadOptionUsage("id", f"Există deja un client cu ID-ul {id}")

    for existing in data.values():
        if int(existing[ "CNP" ]) == cnp:
            raise click.BadParameter(f"Există deja un client cu CNP-ul dat.")

    try:
        parsed_date = datetime.strptime(data_nasterii, "%d.%m.%Y").date()
    except ValueError:
        raise click.BadParameter("Data nașterii trebuie să fie în formatul dd.mm.yyyy")

    client = Client(
        id_entitate=id,
        nume=nume,
        prenume=prenume,
        CNP=cnp,
        data_nasterii=parsed_date
    )

    data[ id ] = client.to_dict()
    write_data(data)
    click.echo(f"Clientul '{nume} {prenume}' a fost adăugat cu succes.")


@cli.command()
@click.argument('id')
@click.pass_context
def delete(ctx, id):
    """Șterge clientul cu ID-ul dat"""
    data = ctx.obj[ 'data' ]

    if id not in data:
        raise click.BadParameter(f"Nu exista niciun client cu ID-ul {id}")

    del data[ id ]
    write_data(data)

    click.echo(f"Clientul cu ID-ul {id} a fost șters cu succes.")


@cli.command()
@click.argument('id')
@click.option('--nume', help="Noul nume")
@click.option('--prenume', help="Noul prenume")
@click.option('--cnp', type=int, help="Noul CNP")
@click.option('--data-nasterii', help="Noua data a nașterii (dd.mm.yyyy)")
@click.pass_context
def update(ctx, id, nume, prenume, cnp, data_nasterii):
    """Actualizează un client existent după ID"""
    data = ctx.obj[ 'data' ]

    if id not in data:
        raise click.BadParameter(f"Nu exista niciun client cu ID-ul {id}")

    client = data[ id ]

    if cnp:
        for key, existing in data.items():
            if key != id and int(existing[ "CNP" ]) == cnp:
                raise click.BadParameter(f"Exista deja un client cu CNP-ul dat.")
        client[ "CNP" ] = cnp

    if data_nasterii:
        try:
            parsed_date = datetime.strptime(data_nasterii, "%d.%m.%Y").date()
            client[ "data_nasterii" ] = parsed_date.strftime("%d.%m.%Y")
        except ValueError:
            raise click.BadParameter("Data nașterii trebuie să fie în formatul dd.mm.yyyy")

    if nume:
        client[ "nume" ] = nume
    if prenume:
        client[ "prenume" ] = prenume

    data[ id ] = client
    write_data(data)

    click.echo(f"Clientul cu ID-ul {id} a fost actualizat.")
