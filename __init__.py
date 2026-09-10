"""Malaphor Generator package."""

try:
    if __package__:
        from .malaphor_logic import MalaphorGenerator
        from .malaphor_ui import MalaphorApp
        from .log_manager import LogManager, log_message
    else:
        from malaphor_logic import MalaphorGenerator
        from malaphor_ui import MalaphorApp
        from log_manager import LogManager, log_message
except Exception:
    # Importing this package during pytest collection can happen without an active package context.
    MalaphorGenerator = None
    MalaphorApp = None
    LogManager = None
    log_message = None

__version__ = '1.0.0'
__all__ = ['MalaphorGenerator', 'MalaphorApp', 'LogManager', 'log_message']