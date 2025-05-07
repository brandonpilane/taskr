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

@click.group()
def cli():
    pass

@cli.command()
@click.argument("title")
def add(title):
    tasks = load_tasks()
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    click.echo(f"Added: {title}")

@cli.command()
def list():
    tasks = load_tasks()
    for i, task in enumerate(tasks, 1):
        status = "✔" if task["done"] else "✘"
        click.echo(f"{i}. {task['title']} [ {status} ]")

@cli.command()
@click.argument("task_number", type=int)
def done(task_number):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"Marked task {task_number} as done.")
    else:
        click.echo("Invalid task number.")
