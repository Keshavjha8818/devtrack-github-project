# DevTrack

A lightweight command-line task manager built with Python. DevTrack stores tasks in a local JSON file and supports adding, listing, completing, and deleting tasks.

## Features

- Add tasks with low, medium, or high priority
- List tasks with their status and priority
- Mark tasks as complete
- Delete tasks by ID
- Persist data in a readable JSON file
- Run without paid APIs, external services, or third-party packages

## Requirements

- Python 3.9 or newer
- Git (only needed if you want to clone or contribute)

## Quick start

```bash
git clone https://github.com/Keshavjha8818/devtrack-github-project.git
cd devtrack-github-project
python3 --version
python3 main.py list
```

No package installation is required because the app uses Python's standard library.

## Usage

Add a task:

```bash
python3 main.py add "Prepare my GitHub portfolio" --priority high
```

List tasks:

```bash
python3 main.py list
```

Mark a task complete using the ID printed when it was created:

```bash
python3 main.py done TASK_ID
```

Delete a task:

```bash
python3 main.py delete TASK_ID
```

Use a different JSON file (useful for experiments and tests):

```bash
python3 main.py --file /tmp/demo-tasks.json add "Try a separate data file"
python3 main.py --file /tmp/demo-tasks.json list
```

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

The tests cover task creation, input validation, completion, deletion, and JSON persistence.

## Project structure

```text
devtrack-github-project/
├── main.py              # CLI commands and task logic
├── tasks.json           # Small sample task dataset
├── tests/
│   └── test_main.py     # Standard-library unit tests
├── requirements.txt     # Documents that no packages are needed
├── .gitignore
├── .env.example
├── LICENSE
└── README.md
```

## Data format

Each task is stored as a JSON object with an ID, title, priority, completion status, and UTC creation timestamp. The default data file is `tasks.json` in the project directory.

## Git workflow demonstrated

This repository is intended as a practical Git learning project. Its development history should show small, meaningful commits, a feature branch, a merge, and a clean final working tree. See the submission notes you create while building the repository; do not squash away the learning history.

## Limitations

- Tasks are stored locally in a JSON file; there is no cloud sync or multi-user support.
- This is a learning project, not a production task-management service.

## License

MIT. See [LICENSE](LICENSE).

## Contributing

1. Create a feature branch from main.
2. Make one focused change at a time.
3. Run the unit tests before committing.
4. Use descriptive commit messages.
5. Merge reviewed changes into main.
