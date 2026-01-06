#!/usr/bin/env python3
"""
Demo script showing the status_list feature.

Run with: python examples/status_list_demo.py
"""

import time

from iris import UI


def main():
    ui = UI()

    ui.header("VM Provisioning Demo")

    # Simulate provisioning multiple VMs
    vms = ["vm-web", "vm-db", "vm-cache", "vm-worker", "vm-monitor"]

    with ui.status_list(vms) as status:
        # Start all VMs as running
        for vm in vms:
            status.update(vm, "running")
            time.sleep(0.3)

        # Simulate provisioning with different outcomes
        time.sleep(0.5)
        status.update("vm-web", "success", detail="10.0.0.2")

        time.sleep(0.8)
        status.update("vm-db", "success", detail="10.0.0.3")

        time.sleep(0.6)
        status.update("vm-cache", "error", detail="timeout connecting to host")

        time.sleep(0.4)
        status.update("vm-worker", "warning", detail="low memory")

        time.sleep(0.5)
        status.update("vm-monitor", "skipped", detail="already exists")

    ui.info("")
    ui.info("Provisioning complete!")
    ui.success("3 VMs ready")
    ui.warning("1 VM has warnings")
    ui.error("1 VM failed")


if __name__ == "__main__":
    main()
