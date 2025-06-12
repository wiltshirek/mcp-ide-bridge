"""Shared data models and utilities for MCP messaging server."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    """Represents a message between clients."""
    from_client_id: str
    content: str
    timestamp: datetime


def format_relative_time(timestamp: datetime) -> str:
    """Format timestamp as relative time (e.g., '5 minutes ago')."""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "just now" 