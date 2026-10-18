#!/usr/bin/env python3
"""Universal launcher: re-execs into the project venv, then runs main.py.

Usage:
    python run.py          # works with any Python on PATH
    ./run.py               # if made executable
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(HERE, "main.py")
VENV_DIR = os.path.join(HERE, "venv")


def _venv_python():
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")


def _in_venv():
    return os.path.realpath(sys.prefix) == os.path.realpath(VENV_DIR)


def main():
    venv_py = _venv_python()
    if os.path.exists(VENV_DIR) and not _in_venv():
        if os.path.exists(venv_py):
            os.chdir(HERE)
            os.execv(venv_py, [venv_py, MAIN] + sys.argv[1:])
        print(f"venv/ exists but {venv_py} is missing or broken.")
        print("Recreate it:  python3 -m venv venv && ./venv/bin/pip install -r requirements.txt")
        sys.exit(1)

    if not os.path.exists(VENV_DIR):
        print("No venv/ directory found.")
        print("Create one and install dependencies:")
        print("  python3 -m venv venv")
        print("  ./venv/bin/pip install -r requirements.txt")
        sys.exit(1)

    os.chdir(HERE)
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    import main as app
    app.main()


if __name__ == "__main__":
    main()
