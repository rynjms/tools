"""
Sample Tool - A demonstration of the tool development paradigm.

This package provides a sample CLI tool that processes files and outputs scores
in the format 'filename: score'.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core import process_file, process_files

__all__ = ["process_file", "process_files"] 