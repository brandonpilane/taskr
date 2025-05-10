import click
import json
from pathlib import Path
from datetime import datetime

TASKS_FILE = Path.home() / ".taskr_tasks.json"

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
    tasks.append({"id": id, "title": title, "status":"todo", "created_at": datetime.now().isoformat()})
    save_tasks(tasks)
    click.echo(click.style("Added", fg="green") + f" task {id}: {title}")

@cli.command()
@click.option('--status', type=click.Choice(['todo', 'in-progress', 'done']), help='Filter tasks by status')
def list(status):
    tasks = load_tasks()

    if status:
        # Filter tasks by status if the --status option is used
        filtered_tasks = [task for task in tasks if task["status"] == status]

        color = (
            "yellow" if status == "todo" else
            "blue" if status == "in-progress" else
            "green"
        )

        if not filtered_tasks:
            click.echo(click.style(f"No tasks with status '{status}'", fg="red"))
            return

        click.echo(click.style(f"  {status.capitalize()}: ", fg=color) + f"{len(filtered_tasks)}\n")
        for i, task in enumerate(filtered_tasks, 1):
            click.echo(f"{i}. {task['title']} (" + click.style(task["status"], fg=color) + ")")

    else:
        if not tasks:
            click.echo(click.style("No tasks found", fg="red"))
            return

        # Display summary counts
        click.echo(f"Total tasks: {len(tasks)}")
        click.echo(click.style("  Todo: ", fg="yellow") + f"{len([t for t in tasks if t['status'] == 'todo'])}")
        click.echo(click.style("  In-progress: ", fg="blue") + f"{len([t for t in tasks if t['status'] == 'in-progress'])}")
        click.echo(click.style("  Done: ", fg="green") + f"{len([t for t in tasks if t['status'] == 'done'])}")
        click.echo()

        # Display all tasks with appropriate colors
        for i, task in enumerate(tasks, 1):
            color = (
                "yellow" if task["status"] == "todo" else
                "blue" if task["status"] == "in-progress" else
                "green"
            )
            click.echo(f"{i}. {task['title']} (" + click.style(task["status"], fg=color) + ")")

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

@cli.command()
@click.argument("id")
def delete(id):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == int(id):
            click.echo(f"Deleted task {id}: {task['title']}")
            tasks.pop(i)

            for j, task in enumerate(tasks):
                if task["id"] > int(id):
                    tasks[j]["id"] -= 1  # Update the IDs of the remaining tasks

            save_tasks(tasks)
            return
    click.echo(f"Task with id {id} not found")
