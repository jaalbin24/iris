# Iris

> Terminal UI library for CLI tools. Named after the Greek goddess of the rainbow.

![Demo](assets/demo.gif)

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-proprietary-red)

## Install

```bash
poetry add git+https://git.kriib.com/Kriib/iris.git#v1.0.0
```

## Quick Start

```python
from iris import header, success, error, warning, info

header("My CLI App")
info("Starting process...")
success("Done!")
warning("Check disk space")
error("Something failed")
```

## Features

- **Colored output** with icons (`success`, `error`, `warning`, `info`, `hint`, `debug`)
- **Full-width danger banners** for critical alerts via `danger_banner()`
- **Live status tracking** with animated spinners via `status_list()`
- **Progress tracking** for multi-step operations via `progress()`
- **Interactive prompts** (`confirm`, `prompt`, `prompt_choice`)
- **Table rendering** with auto-sized columns
- **Formatting utilities** (`format_duration`, `format_size`, `format_age`)
- **Thread-safe** by default

<details>
<summary><strong>Examples</strong></summary>

### Status List (Live Updates)

```python
from iris import UI

ui = UI()
with ui.status_list(["web", "db", "cache"]) as status:
    status.update("web", "running")
    # ... do work ...
    status.update("web", "success", "10.0.0.2")
    status.update("db", "error", "timeout")
```

### Progress Tracking

```python
from iris import UI

ui = UI(verbose=True)
with ui.progress(["PostgreSQL", "MinIO"]) as p:
    p.start("PostgreSQL")
    ui.command("pg_dump kriib_db")
    p.complete("PostgreSQL", "1.2 GB")

    p.start("MinIO")
    p.complete("MinIO", "1.1 GB")
```

### Tables

```python
from iris import Table

table = Table(["Name", "Status", "Size"])
table.add_row("backup-01", "OK", "2.3 GB")
table.add_row("backup-02", "OK", "1.8 GB")
table.render()
```

### Prompts

```python
from iris import confirm, prompt, prompt_choice

if confirm("Continue?", default=False):
    password = prompt("Password", mask=True)
    idx = prompt_choice("Target", ["postgres", "minio", "all"])
```

### Utilities

```python
from iris import format_duration, format_size, format_age
from datetime import datetime, timedelta

format_duration(90)       # "1m 30s"
format_size(1536 * 1024 * 1024)  # "1.5 GB"
format_age(datetime.now() - timedelta(hours=4))  # "4 hours ago"
```

### Box & Danger Banner

```python
from iris import box, danger_banner

# Double-line bordered box (no background)
box("NOTICE")

# Red background danger banner
danger_banner("CRITICAL ALERT")

# Multi-line support
box("Line 1\nLine 2")
```

</details>

<details>
<summary><strong>API Reference</strong></summary>

### Output Functions

| Function | Description | Output |
|----------|-------------|--------|
| `header(msg)` | Section header | `═══ Title ═══` |
| `success(msg)` | Success message | `[✓] Done` |
| `error(msg)` | Error (stderr) | `[x] Failed` |
| `warning(msg)` | Warning | `[!] Warning` |
| `info(msg)` | Info | `[i] Info` |
| `hint(msg)` | Hint | `[+] Try this` |
| `command(cmd)` | Command | `[>] Running: cmd` |
| `debug(msg, enabled)` | Debug (if enabled) | `[DEBUG] msg` |
| `secure(msg)` | Security message | `[S] Encrypted` |
| `dry_run(msg)` | Dry-run | `[DRY-RUN] Would: msg` |
| `step(cur, total, msg)` | Step | `[1/3] Step` |
| `duration(secs)` | Elapsed time | `[TIME] 42.5s` |
| `box(msg, bg, fg)` | Bordered box | `╔═══╗ ║msg║ ╚═══╝` |
| `danger_banner(msg)` | Red bordered box | `box()` with red background |

### UI Class

```python
UI(interactive=True, verbose=False, debug=False)
```

- `interactive`: If `False`, prompts return defaults without asking
- `verbose`: If `True`, `ui.command()` outputs are shown
- `debug`: If `True`, `ui.debug()` outputs are shown

### Table Class

```python
table = Table(columns: list[str])
table.add_row(*values: str)
table.render()              # Print to stdout
table.render_to_string()    # Return as string
```

</details>

<details>
<summary><strong>Development</strong></summary>

```bash
poetry install
poetry run pytest
poetry run pytest --cov=iris
```

### Style Guide

- ASCII-only except: `═` (header), `✓` (success), `─` (table)
- No emojis
- Thread-safe by default
- Consistent prefix format: `[✓]`, `[x]`, `[!]`, `[i]`, `[?]`, `[>]`, `[S]`, `[+]`

</details>

## License

Proprietary - Kriib Internal Use Only
