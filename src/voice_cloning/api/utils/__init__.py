"""
Utility functions for the FastAPI application.
"""

from datetime import datetime
import os
import asyncio


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat() + "Z"


async def cleanup_file(filepath: str, delay: int = 300):
    """
    Delete a file after a delay (in seconds).
    
    Args:
        filepath: Path to file to delete
        delay: Delay in seconds before deletion
    """
    await asyncio.sleep(delay)
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"🗑️ Cleaned up: {filepath}")
    except Exception as e:
        print(f"⚠️ Failed to cleanup {filepath}: {str(e)}")
