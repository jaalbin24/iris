# Iris

Terminal UI library for CLI tools. Named after the Greek goddess of the rainbow and messenger of the gods.

## Installation

```bash
# From git repository
poetry add git+https://git.kriib.com/Kriib/iris.git#v1.0.0

# Or in pyproject.toml
[tool.poetry.dependencies]
iris = { git = "https://git.kriib.com/Kriib/iris.git", tag = "v1.0.0" }
```

## Quick Start

### Stateless Usage

```python
from iris import header, success, error, info, warning

header("Creating Backup")
info("Running: pg_dump ...")
success("Backup complete")
warning("Disk space low")
error("Connection failed")
```

### Stateful Usage (with UI Context)

```python
from iris import UI

ui = UI(interactive=True, verbose=True, debug=False)

ui.header("Creating Backup")

with ui.progress(["PostgreSQL", "MinIO"]) as p:
    p.start("PostgreSQL")
    ui.command("pg_dump kriib_db")  # Only shows if verbose=True
    p.complete("PostgreSQL", "1.2 GB")

    p.start("MinIO")
    p.complete("MinIO", "1.1 GB")

ui.success("Backup complete")
```

### Tables

```python
from iris import Table

table = Table(["Batch-ID", "Created", "Status", "Size"])
table.add_row("20260103-020000", "2026-01-03 02:00:00", "OK", "2.3 GB")
table.add_row("20260102-020000", "2026-01-02 02:00:00", "OK", "2.3 GB")
table.render()
```

Output:
```
Batch-ID         Created               Status   Size
───────────────────────────────────────────────────────
20260103-020000  2026-01-03 02:00:00   OK       2.3 GB
20260102-020000  2026-01-02 02:00:00   OK       2.3 GB
```

### User Prompts

```python
from iris import confirm, prompt, prompt_choice

# Yes/no confirmation
if confirm("Continue with restore?", default=False):
    do_restore()

# Text input (with optional masking for passwords)
password = prompt("Repository password", mask=True)

# Choice selection
idx = prompt_choice("Select target", ["postgres", "minio", "all"])
```

### Utilities

```python
from iris import format_duration, format_size, format_age
from datetime import datetime, timedelta

format_duration(90)      # "1m 30s"
format_duration(3661)    # "1h 1m"

format_size(1536 * 1024 * 1024)  # "1.5 GB"

format_age(datetime.now() - timedelta(hours=4))  # "4 hours ago"
```

## API Reference

### Output Functions

| Function | Description | Example Output |
|----------|-------------|----------------|
| `header(msg)` | Section header with lines | `═══ Title ═══` |
| `success(msg)` | Success with checkmark | `[✓] Done` |
| `error(msg)` | Error with X (to stderr) | `[x] Failed` |
| `warning(msg)` | Warning with exclamation | `[!] Warning` |
| `info(msg)` | Info message | `[i] Info` |
| `hint(msg)` | Hint with plus | `[+] Try this` |
| `command(cmd)` | Command being run | `[>] Running: cmd` |
| `debug(msg, enabled)` | Debug (if enabled) | `[DEBUG] msg` |
| `secure(msg)` | Security message | `[S] Encrypted` |
| `dry_run(msg)` | Dry-run indicator | `[DRY-RUN] Would: msg` |
| `step(cur, total, msg)` | Step indicator | `[1/3] Step` |
| `duration(secs)` | Time elapsed | `[TIME] 42.5s` |

### UI Class

```python
UI(interactive=True, verbose=False, debug=False)
```

- `interactive`: If False, prompts return defaults without asking
- `verbose`: If True, `ui.command()` outputs are shown
- `debug`: If True, `ui.debug()` outputs are shown

### Table Class

```python
table = Table(columns: list[str])
table.add_row(*values: str)
table.render()  # Print to stdout
table.render_to_string()  # Return as string
```

## Style Guide

- ASCII-only except approved unicode: `═` (header), `✓` (success), `─` (table separator)
- No emojis
- Thread-safe by default
- Consistent prefix format: `[✓]`, `[x]`, `[!]`, `[i]`, `[?]`, `[>]`, `[S]`, `[+]`

## Development

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=iris
```

## License

Proprietary - Kriib Internal Use Only
