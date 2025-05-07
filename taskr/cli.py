import click
import json
from pathlib import Path

TASKS_FILE = Path.home() / ".taskr_tasks.json"  # Better than local file

def load_tasks():
    if TASKS_FILE.exists():
        return json.loads(TASKS_FILE.read_text())
    return []

def save_tasks(tasks):
    TASKS_FILE.write_text(json.dumps(tasks, indent=2))

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None: # If no subcommand is provided
        click.echo("Taskr - A simple task manager")
        click.echo(cli.get_help(ctx))  # Show help message

@cli.command()
@click.argument("title")
def add(title):
    tasks = load_tasks()
    id = len(tasks) + 1
    tasks.append({"id": id, "title": title, "status":"todo"})
    save_tasks(tasks)
    click.echo(f"Added: {title}")

@cli.command()
def list():
    tasks = load_tasks()
    for i, task in enumerate(tasks, 1):
        status = "✓" if task["done"] else "✕"
        click.echo(f"{i}. {task['title']} [ {status} ]")
