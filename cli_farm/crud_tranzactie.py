import json
from collections import defaultdict
from datetime import date, datetime

import click
from pathlib import Path

from tabulate import tabulate
from pydantic import BaseModel


class Entitate(BaseModel):
    id_entitate: str


class Tranzactie(Entitate):
    id_medicament: str
    id_card_client: str
    nr_bucati: int
    data_ora: datetime

    def to_dict(self):
        return {
            "id_entitate": self.id_entitate,
            "id_medicament": self.id_medicament,
            "id_card_client": self.id_card_client,
            "nr_bucati": self.nr_bucati,
            "data_ora": self.data_ora.strftime("%d.%m.%Y %H:%M")
        }


# ========= File Path ==========
TRANZACTIE_FILE = Path.home() / "PycharmProjects/Farmacie/tranzactie.json"
MEDICAMENT_FILE = Path.home() / "PycharmProjects/Farmacie/medicament.json"
CLIENT_FILE = Path.home() / "PycharmProjects/Farmacie/client.json"


def read_data():
    if TRANZACTIE_FILE.exists():
        with open(TRANZACTIE_FILE) as f:
            return json.load(f)
    return {}


def write_data(data):
    with open(TRANZACTIE_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def exists_in_file(file_path: Path, id_check: str) -> bool:
    if file_path.exists():
        with open(file_path) as f:
            data = json.load(f)
        return id_check in data
    return False


# ========= CLI =========
@click.group()
@click.pass_context
def cli(ctx):
    """Tranzactie CLI group for CRUD operations"""
    ctx.ensure_object(dict)
    ctx.obj[ 'data' ] = read_data()


@cli.command()
@click.pass_context
def show(ctx):
    """Afișează toate tranzacțiile înregistrate"""
    data = ctx.obj[ 'data' ]
    if not data:
        click.echo("Nu există nicio tranzacție înregistrată.")
        return

    tranzactii = [ ]
    for raw in data.values():
        raw.pop("py/object", None)
        tranzactie = Tranzactie(
            **{
                **raw,
                "data_ora": datetime.strptime(raw[ "data_ora" ], "%d.%m.%Y %H:%M")
            }
        )
        tranzactii.append([
            tranzactie.id_entitate,
            tranzactie.id_medicament,
            tranzactie.id_card_client,
            tranzactie.nr_bucati,
            tranzactie.data_ora.strftime("%d.%m.%Y %H:%M")
        ])

    headers = [ "ID", "ID Medicament", "ID Client", "Nr Bucăți", "Data și Ora" ]
    click.echo(tabulate(tranzactii, headers=headers, tablefmt="simple_outline"))


@cli.command()
@click.option('--id', prompt="ID", help="ID-ul tranzacției")
@click.option('--id-medicament', prompt="ID Medicament", help="ID-ul medicamentului vândut")
@click.option('--id-card-client', prompt="ID Client (sau lasă gol dacă nu există)", default="",
              show_default=False)
@click.option('--nr-bucati', prompt="Număr de bucăți", type=int, help="Numărul de bucăți vândute")
@click.option('--data-ora', prompt="Data și ora (dd.mm.yyyy HH:MM)", help="Data și ora tranzacției")
@click.pass_context
def add(ctx, id, id_medicament, id_card_client, nr_bucati, data_ora):
    """Adaugă o nouă tranzacție"""
    data = ctx.obj[ 'data' ]

    if id in data:
        raise click.BadOptionUsage("id", f"Există deja o tranzacție cu ID-ul {id}")
    if nr_bucati <= 0:
        raise click.BadParameter("Numărul de bucăți trebuie să fie mai mare decât 0.")

    # Validate date
    try:
        parsed_datetime = datetime.strptime(data_ora, "%d.%m.%Y %H:%M")
    except ValueError:
        raise click.BadParameter("Data și ora trebuie să fie în formatul dd.mm.yyyy HH:MM")

    # Validate medicament exists
    if not exists_in_file(MEDICAMENT_FILE, id_medicament):
        raise click.BadParameter(f"Nu există niciun medicament cu ID-ul {id_medicament}")

    # Validate card client if provided
    if id_card_client.strip():
        if not exists_in_file(CLIENT_FILE, id_card_client):
            raise click.BadParameter(f"Nu există niciun client cu ID-ul {id_card_client}")

    tranzactie = Tranzactie(
        id_entitate=id,
        id_medicament=id_medicament,
        id_card_client=id_card_client.strip(),
        nr_bucati=nr_bucati,
        data_ora=parsed_datetime
    )

    data[ id ] = tranzactie.to_dict()
    write_data(data)
    click.echo(f"Tranzacția cu ID-ul '{id}' a fost adăugată cu succes.")


@cli.command()
@click.argument('id')
@click.pass_context
def delete(ctx, id):
    """Șterge tranzacția cu ID-ul dat"""
    data = ctx.obj[ 'data' ]

    if id not in data:
        raise click.BadParameter(f"Tranzacția cu ID-ul {id} nu există.")

    del data[ id ]
    write_data(data)
    click.echo(f"Tranzacția cu ID-ul {id} a fost ștearsă cu succes.")


@cli.command()
@click.argument('id')
@click.option('--id-medicament', help="ID nou pentru medicament")
@click.option('--id-card-client', help="ID nou pentru client (daca exista)")
@click.option('--nr-bucati', type=int, help="Număr nou de bucăți")
@click.option('--data-ora', help="Data și ora nouă (dd.mm.yyyy HH:MM)")
@click.pass_context
def update(ctx, id, id_medicament, id_card_client, nr_bucati, data_ora):
    """Actualizează o tranzacție existentă după ID"""
    data = ctx.obj[ 'data' ]

    if id not in data:
        raise click.BadParameter(f"Tranzacția cu ID-ul {id} nu există.")

    tranzactie = data[ id ]

    # Validare ID medicament
    if id_medicament:
        if not exists_in_file(MEDICAMENT_FILE, id_medicament):
            raise click.BadParameter(f"Nu există niciun medicament cu ID-ul {id_medicament}")
        tranzactie[ "id_medicament" ] = id_medicament

    # Validare ID card client
    if id_card_client is not None:
        id_card_client = id_card_client.strip()
        if id_card_client:
            if not exists_in_file(CLIENT_FILE, id_card_client):
                raise click.BadParameter(f"Nu există niciun client cu ID-ul {id_card_client}")
        tranzactie[ "id_card_client" ] = id_card_client

    # Validare număr bucăți
    if nr_bucati is not None:
        if nr_bucati <= 0:
            raise click.BadParameter("Numărul de bucăți trebuie să fie mai mare decât 0.")
        tranzactie[ "nr_bucati" ] = nr_bucati

    if data_ora:
        try:
            parsed_datetime = datetime.strptime(data_ora, "%d.%m.%Y %H:%M")
            tranzactie[ "data_ora" ] = parsed_datetime.strftime("%d.%m.%Y %H:%M")
        except ValueError:
            raise click.BadParameter("Data și ora trebuie să fie în formatul dd.mm.yyyy HH:MM")

    data[ id ] = tranzactie
    write_data(data)

    click.echo(f"Tranzacția cu ID-ul {id} a fost actualizată.")


def read_file(path: Path) -> dict:
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def write_file(path: Path, data: dict):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


@click.group(help="Funcționalități extinse pentru tranzacții")
def operations():
    pass


@operations.command(name="show-interval", help="Afișează tranzacțiile dintr-un interval de zile")
@click.option('--de-la', required=True, help="Data de început (format dd.mm.yyyy)")
@click.option('--pana-la', required=True, help="Data de sfârșit (format dd.mm.yyyy)")
def show_interval(de_la, pana_la):
    tranzactii = read_file(TRANZACTIE_FILE)

    try:
        start_date = datetime.strptime(de_la, "%d.%m.%Y").date()
        end_date = datetime.strptime(pana_la, "%d.%m.%Y").date()
    except ValueError:
        raise click.BadParameter("Formatul datei trebuie să fie dd.mm.yyyy")

    rezultate = [ ]
    for t in tranzactii.values():
        data_ora = datetime.strptime(t[ "data_ora" ], "%d.%m.%Y %H:%M")
        if start_date <= data_ora.date() <= end_date:
            rezultate.append([
                t[ "id_entitate" ],
                t[ "id_medicament" ],
                t[ "id_card_client" ],
                t[ "nr_bucati" ],
                t[ "data_ora" ]
            ])

    if not rezultate:
        click.echo("Nu există tranzacții în intervalul specificat.")
        return

    headers = [ "ID", "ID Medicament", "ID Client", "Nr Bucăți", "Data și Ora" ]
    click.echo(tabulate(rezultate, headers=headers, tablefmt="simple_outline"))


@operations.command(name="top-vanzari", help="Afișează medicamentele ordonate descrescător după vânzări")
def top_vanzari():
    tranzactii = read_file(TRANZACTIE_FILE)
    medicamente = read_file(MEDICAMENT_FILE)

    vanzari = defaultdict(int)

    for t in tranzactii.values():
        id_med = t[ "id_medicament" ]
        vanzari[ id_med ] += int(t[ "nr_bucati" ])

    if not vanzari:
        click.echo("Nu există vânzări înregistrate.")
        return

    sortate = sorted(vanzari.items(), key=lambda x: x[ 1 ], reverse=True)

    rezultat = [ ]
    for id_med, total in sortate:
        nume = medicamente.get(id_med, {}).get("nume", "Nume necunoscut")
        rezultat.append([ id_med, nume, total ])

    headers = [ "ID Medicament", "Nume Medicament", "Total bucati vandute" ]
    click.echo(tabulate(rezultat, headers=headers, tablefmt="simple_outline"))


@operations.command(name="delete-interval", help="Șterge toate tranzacțiile dintr-un interval de zile")
@click.option('--de-la', required=True, help="Data de început (format dd.mm.yyyy)")
@click.option('--pana-la', required=True, help="Data de sfârșit (format dd.mm.yyyy)")
def delete_interval(de_la, pana_la):
    """Șterge toate tranzacțiile dintr-un interval de zile"""
    tranzactii = read_file(TRANZACTIE_FILE)

    try:
        start_date = datetime.strptime(de_la, "%d.%m.%Y").date()
        end_date = datetime.strptime(pana_la, "%d.%m.%Y").date()
    except ValueError:
        raise click.BadParameter("Formatul datei trebuie să fie dd.mm.yyyy")

    initial_count = len(tranzactii)

    tranzactii_filtrate = {
        k: v for k, v in tranzactii.items()
        if not (start_date <= datetime.strptime(v[ "data_ora" ], "%d.%m.%Y %H:%M").date() <= end_date)
    }

    sterse = initial_count - len(tranzactii_filtrate)
    write_file(TRANZACTIE_FILE, tranzactii_filtrate)

    click.echo(f"Au fost șterse {sterse} tranzacții din intervalul {de_la} - {pana_la}.")
