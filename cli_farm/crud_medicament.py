import json
import click
from pathlib import Path

from tabulate import tabulate
from pydantic import BaseModel, field_validator


class Entitate(BaseModel):
    id_entitate: str


class Medicament(Entitate):
    nume: str
    producator: str
    pret: float
    reteta: str

    @field_validator("pret")
    @classmethod
    def validate_pret(cls, pret):
        if pret < 0:
            raise ValueError("pret must be greater than or equal to 0")
        return pret

    def to_dict(self):
        return {
            "id_entitate": self.id_entitate,
            "nume": self.nume,
            "producator": self.producator,
            "pret": self.pret,
            "reteta": self.reteta,
        }


# ========= File Path ==========
MEDICAMENT_FILE = Path.home() / "PycharmProjects/Farmacie/medicament.json"


def read_data():
    if MEDICAMENT_FILE.exists():
        with open(MEDICAMENT_FILE) as f:
            return json.load(f)
    return {}


def write_data(data):
    with open(MEDICAMENT_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ========= CLI =========
@click.group()
@click.pass_context
def cli(ctx):
    """Medicament CLI group for CRUD operations"""
    ctx.ensure_object(dict)
    ctx.obj[ "data" ] = read_data()


@cli.command()
@click.pass_context
def show(ctx):
    """Afișează toate medicamentele din repository"""
    data = ctx.obj[ "data" ]
    if not data:
        click.echo("Nu există medicamente salvate.")
        return

    medicamente = [ ]
    for raw in data.values():
        raw.pop("py/object", None)
        med = Medicament(**raw)
        medicamente.append(
            [
                med.id_entitate,
                med.nume,
                med.producator,
                f"{med.pret:.2f}",
                med.reteta,
            ]
        )

    headers = [ "ID", "Nume", "Producător", "Preț", "Rețetă" ]
    click.echo(
        tabulate(medicamente, headers=headers, tablefmt="simple_outline")
    )


@cli.command()
@click.option("--id", prompt="ID", help="ID")
@click.option("--nume", prompt="Nume",
              help="Numele medicamentului")
@click.option(
    "--producator", prompt="Producător",
    help="Numele producătorului"
)
@click.option(
    "--pret", prompt="Preț", type=float,
    help="Prețul medicamentului"
)
@click.option(
    "--reteta",
    prompt="Necesită rețetă",
    type=click.Choice([ "da", "nu" ]),
    help="Necesită rețetă",
)
@click.pass_context
def add(ctx, id, nume, producator, pret, reteta):
    """Adaugă un nou medicament în repository"""
    data = ctx.obj[ "data" ]

    if id in data:
        raise click.BadOptionUsage(
            "id", f"Există deja un medicament cu ID-ul {id}"
        )
    if pret < 0:
        raise click.BadParameter("Prețul nu poate fi negativ.")

    med = Medicament(
        id_entitate=id,
        nume=nume,
        producator=producator,
        pret=pret,
        reteta=reteta,
    )

    data[ id ] = med.to_dict()
    write_data(data)

    click.echo(f"Medicamentul '{nume}' a fost adăugat cu succes.")


@cli.command()
@click.argument("id")
@click.pass_context
def delete(ctx, id):
    """Șterge medicamentul cu ID-ul dat"""
    data = ctx.obj[ "data" ]

    if id not in data:
        raise click.BadParameter(f"Medicamentul cu ID-ul {id} nu există.")

    del data[ id ]
    write_data(data)

    click.echo(f"Medicamentul cu ID-ul {id} a fost șters cu succes.")


@cli.command()
@click.argument("id")
@click.option("--nume", help="Noul nume al medicamentului")
@click.option("--producator", help="Noul producător")
@click.option("--pret", type=float, help="Noul preț")
@click.option(
    "--reteta", type=click.Choice([ "da", "nu" ]),
    help="Necesită rețetă (da/nu)"
)
@click.pass_context
def update(ctx, id, nume, producator, pret, reteta):
    """Actualizează un medicament existent după ID"""
    data = ctx.obj[ "data" ]

    if id not in data:
        raise click.BadParameter(f"Medicamentul cu ID-ul {id} nu există.")

    med = data[ id ]

    updates = {
        "nume": nume,
        "producator": producator,
        "pret": pret,
        "reteta": reteta if reteta else None,
    }

    for key, value in updates.items():
        if value is not None:
            med[ key ] = value

    data[ id ] = med
    write_data(data)

    click.echo(f"Medicamentul cu ID-ul {id} a fost actualizat.")
