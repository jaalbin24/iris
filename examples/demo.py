#!/usr/bin/env python3
"""Demo script for README GIF recording."""
import time

from iris import UI, Table, danger_banner, header, success, error, warning, info


def main():
    # 1. Basic output functions
    header("Iris Demo")
    success("Operation completed")
    warning("Disk space low")
    error("Connection failed")
    info("Retrying in 5s...")

    print()

    # 2. Live status list with spinner
    ui = UI()
    services = ["api-server", "database", "cache", "worker"]

    with ui.status_list(services) as status:
        for svc in services:
            status.update(svc, "running")
            time.sleep(0.4)

        time.sleep(0.3)
        status.update("api-server", "success", "healthy")
        time.sleep(0.5)
        status.update("database", "success", "connected")
        time.sleep(0.4)
        status.update("cache", "warning", "high memory")
        time.sleep(0.3)
        status.update("worker", "error", "timeout")

    print()

    # 3. Table output
    table = Table(["Service", "Status", "Uptime"])
    table.add_row("api-server", "OK", "12d 4h")
    table.add_row("database", "OK", "12d 4h")
    table.add_row("cache", "WARN", "2h 15m")
    table.render()

    print()

    # 4. Danger banner (full-width red alert)
    danger_banner("CRITICAL ALERT")


if __name__ == "__main__":
    main()
