#!/usr/bin/env python3
"""
Raystack command-line utility for administrative tasks.
This script allows running raystack commands without installing the package.
"""
import os
import sys

# Add the src directory to Python path so we can import raystack without installation
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

if __name__ == "__main__":
    try:
        from raystack.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Raystack. Are you sure the src directory exists and "
            "contains the raystack package?"
        ) from exc
    execute_from_command_line(sys.argv)
