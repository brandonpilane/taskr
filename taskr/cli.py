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
        click.echo(
            click.style("TASKR", fg="red", bold=True) + 
            " - A simple task manager"
        )
        click.echo(cli.get_help(ctx))  # Show help message

@cli.command()
@click.argument("title")
def add(title):
    tasks = load_tasks()
    id = len(tasks) + 1
    tasks.append({"id": id, "title": title, "status":"todo"})
    save_tasks(tasks)
    click.echo(click.style("Added", fg="green") + f" task {id}: {title}")

@cli.command()
def list():
    tasks = load_tasks()
    click.echo("-" * 40)
    click.echo(f"Total tasks: {len(tasks)}")
    click.echo(click.style("  Todo: ", fg="yellow") + f"{len([task for task in tasks if task['status'] == 'todo'])}")
    click.echo(click.style("  In-progress: ", fg="blue") + f"{len([task for task in tasks if task['status'] == 'in-progress'])}")
    click.echo(click.style("  Done: ", fg="green") + f"{len([task for task in tasks if task['status'] == 'done'])}")
    click.echo("-" * 40 + "\n")
    for i, task in enumerate(tasks, 1):
        if task["status"] == "todo":
            color = "yellow"
        elif task["status"] == "in-progress":
            color = "blue"
        elif task["status"] == "done":
            color = "green"
        else:
            color = "red"
        click.echo(f"{i}. {task['title']} (" + click.style(task["status"], fg=color) + ")")
    click.echo("\n" + "-" * 40)

@cli.command()
@click.argument("id")
@click.argument("title")
def update(id, title):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == int(id):
            changed_title = tasks[i]["title"]
            tasks[i]["title"] = title
            save_tasks(tasks)
            click.echo(f"Updated task {id}:\n{changed_title}" + click.style(" → ", fg="green") + f"{title}")
            return
    click.echo(f"Task with id {id} not found")
