"""
Ask Jane — a climate-aware garden planner for Saved by the Plate.
"""

__version__ = "4.2.0"

from .core.agent import AGIAgent
from .cli import main

__all__ = ['AGIAgent', 'main']
