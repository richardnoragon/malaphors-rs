"""Malaphor Generator package."""

from .malaphor_logic import MalaphorGenerator
from .malaphor_ui import MalaphorApp
from .log_manager import LogManager, log_message

__version__ = '1.0.0'
__all__ = ['MalaphorGenerator', 'MalaphorApp', 'LogManager', 'log_message']