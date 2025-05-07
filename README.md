# `taskr` – A Python CLI Task Tracker

A minimal, dependency-free command-line tool written in Python to track your to-dos directly from the terminal. Create, update, and manage tasks using simple commands — no database or external libraries required. Tasks are stored locally in a JSON file.

---

## Features

* Add, update, and delete tasks
* Mark tasks as **todo**, **in-progress**, or **done**
* List all tasks or filter by status
* Persistent local storage using `tasks.json`
* Zero dependencies — uses Python's standard library

---

## Why `taskr`?

Most task management apps are overkill for simple to-dos. `taskr` gives you the power of a simple tracker, accessible entirely via your terminal — fast, scriptable, and distraction-free.

---

## 🛠 Installation

### 🔹 Option 1: Install via `pip`

```bash
git clone https://github.com/yourusername/taskr.git
cd taskr
pip install .
```

Now you can use `taskr` as a command from anywhere:

```bash
taskr add "Write project README"
```

### 🔹 Option 2: Make it Executable Locally

1. Add the shebang to the top of `taskr.py`:

   ```python
   #!/usr/bin/env python3
   ```

2. Rename the file to `taskr` (no extension) and make it executable:

   ```bash
   chmod +x taskr
   mv taskr ~/.local/bin/
   ```

Make sure `~/.local/bin` is in your PATH.

---

## 🧾 Task Format

Each task in `tasks.json` includes:

```json
{
  "id": 1,
  "description": "Write unit tests",
  "status": "todo",
  "createdAt": "2025-05-06T14:00:00Z",
  "updatedAt": "2025-05-06T14:30:00Z"
}
```

---

## 🧪 Usage

```bash
# Add a new task
taskr add "Refactor codebase"

# Update a task
taskr update 1 "Refactor and document codebase"

# Delete a task
taskr delete 1

# Mark a task
taskr mark-in-progress 2
taskr mark-done 2

# List all tasks
taskr list

# List by status
taskr list todo
taskr list in-progress
taskr list done
```

---

## 📂 File Structure

```
taskr/
├── taskr/
│   └── __main__.py  # Entry point
├── tasks.json       # Auto-generated task database
├── setup.py         # For pip install
└── README.md
```

---

## 📦 Dependencies

None. Uses only:

* `argparse`
* `json`
* `os`
* `datetime`

---

## 🧠 Getting Started with Development

1. Fork and clone this repo.
2. Edit `taskr/__main__.py` to modify CLI behavior.
3. Run locally with:

   ```bash
   python -m taskr add "Test a feature"
   ```
   
4. Create a PR with improvements or fixes.

---

## 💡 Future Ideas

* Tagging system for tasks
* Due dates and reminders
* Integration with shell prompts (e.g., show active task)

---

## 📄 License

[MIT](./LICENSE)
