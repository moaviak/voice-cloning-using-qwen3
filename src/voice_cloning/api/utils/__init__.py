"""
Utility functions for the FastAPI application.
"""

from datetime import datetime
import os
import asyncio
from typing import Callable, TypeVar

T = TypeVar("T")


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat() + "Z"


async def run_inference(func: Callable[..., T], *args, **kwargs) -> T:
    """
    Run a blocking model/inference call in the default thread pool.

    Keeps the asyncio event loop free so concurrent requests can start
    inference without waiting for another request to finish.
    """
    return await asyncio.to_thread(func, *args, **kwargs)


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
