import click

from pathlib import Path
from datetime import datetime

NOTES_DB = Path.home() / ".notes"/ "notes.txt"
DISPLAY_FMT = "{:3} {:16} {:16} {:40}"

def print_header():
    click.echo(DISPLAY_FMT.format("ID", "Created", "Updated", "Contents"))
    click.echo(DISPLAY_FMT.format("-"*3, "-"*16, "-"*16, "-"*40))

def print_note(idx, note):
    created, updated, contents = note.split("\t")
    dt_frm = "%b-%d %I:%M %p"
    created = datetime.fromisoformat(created).strftime(dt_frm)
    updated = datetime.fromisoformat(updated).strftime(dt_frm)
    click.echo(DISPLAY_FMT.format(idx, created, updated, contents))

def load_notes():
    notes = []
    with open(NOTES_DB) as fo:
        for line in fo:
            notes.append(line.strip())
    return notes

def save_notes(notes):
    with open(NOTES_DB, 'w') as fo:
        for note in notes:
            fo.write(f"{note}\n")

@click.group()
def main(ctx):
    """Program for managing notes"""
    if not NOTES_DB.parent.exists():
        NOTES_DB.parent.mkdir()
        NOTES_DB.touch()

    ctx.ensure_object(dict)

    ctx.obj['notes'] = load_notes()

@main.command()
@click.pass_context
def show(ctx):
    """Show notes"""
    notes = ctx.obj['notes']
    print_header()
    for i, note in enumerate(notes, start=1):
        print_note(i, note)


@main.command()
@click.pass_context
def add(ctx):
    """Add notes"""
    notes = ctx.obj['notes']
    created = datetime.now().isoformat()
    contents = click.prompt("note Contents")
    notes.append(f"{created}\t {created}\t {contents}")

    save_notes(notes)

@main.command()
@click.pass_context
def update(ctx):
    """Update notes"""
    pass

@main.command()
@click.pass_context
def delete(ctx):
    """Delete notes"""
    pass



