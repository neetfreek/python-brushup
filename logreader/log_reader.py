#!/usr/bin/env python
"""Read selected log files, copying those with failures and errors into
./logs{log file name}.
Lines of interest are written to ./logs{log file name}_issues.log
"""

from pathlib import Path

DIR_READ_LOGS = Path("./logs")
PATH_READ_LOGS = Path.cwd() / DIR_READ_LOGS

log_dir = Path('/var/log')
log_files = [Path("boot.log"), "messages.log", "auth.log", "daemon.log",
             "kern.log"]


def _create_logs_dir():
    # Create dir for read logs if it doesn't exist.
    if not PATH_READ_LOGS.is_dir():
        print(f"PATH_READ_LOGS does not exist")
        Path(PATH_READ_LOGS).mkdir(parents=True, exist_ok=True)


print(Path.cwd())
_create_logs_dir()
