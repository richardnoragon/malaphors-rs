# Malaphor Generator

Malaphor Generator is a Python desktop application for creating playful malaphors by blending phrases, idioms, and proverbs. The project also includes a Rust/Tauri-based implementation in the [malaphor-rs](malaphor-rs) directory.

## What this project includes

- A Tkinter-based Python app for generating and managing malaphors
- A phrase database stored in JSON
- Logging and settings management interfaces
- A Rust/Tauri implementation for experimentation and desktop packaging

## Features

- Generate random malaphors by combining the beginning of one phrase with the end of another
- Manually select source phrases for combination
- Manage phrases, history, and favorites
- Import and export phrase collections and logs
- Inspect and edit JSON-based settings through a GUI

## Requirements

- Python 3.10+
- Tkinter (included with most Python installations on Windows/macOS/Linux)
- Optional: Rust and Cargo if you want to build the Rust/Tauri app

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd malaphors-rs
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Python app:
   ```bash
   python main.py
   ```

## Project structure

- [main.py](main.py): entry point for the Python application
- [malaphor_logic.py](malaphor_logic.py): generation and phrase-management logic
- [malaphor_ui.py](malaphor_ui.py): Tkinter-based UI
- [malaphors.json](malaphors.json): default phrase dataset
- [settings_manager.py](settings_manager.py): settings editor
- [log_manager.py](log_manager.py): logging interface
- [malaphor-rs](malaphor-rs): Rust/Tauri implementation

## Running tests

The project includes pytest-based tests.

```bash
pytest
```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).