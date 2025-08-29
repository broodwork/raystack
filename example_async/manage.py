#!/usr/bin/env python
"""Raystack's command-line utility for administrative tasks."""
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../src'))
sys.path.insert(0, os.path.abspath('.'))


def main():
    """Run administrative tasks."""
    os.environ.setdefault('RAYSTACK_SETTINGS_MODULE', 'config.settings')
    try:
        from raystack.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Raystack. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
