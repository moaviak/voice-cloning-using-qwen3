#!/usr/bin/env python3
"""
FastAPI runner script for Voice Cloning API.

This script starts the FastAPI application with proper configuration and error handling.

Usage:
    python scripts/run_api.py                    # Run on default host:port (0.0.0.0:8000)
    python scripts/run_api.py --port 5000       # Run on custom port
    python scripts/run_api.py --host localhost  # Run on localhost only
    python scripts/run_api.py --reload          # Enable auto-reload for development
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def main():
    parser = argparse.ArgumentParser(
        description="Start the Voice Cloning FastAPI server"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on code changes (development mode)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes (default: 1)"
    )
    parser.add_argument(
        "--log-level",
        choices=["critical", "error", "warning", "info", "debug"],
        default="info",
        help="Log level (default: info)"
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("🚀 Starting Voice Cloning FastAPI Server")
    print("=" * 80)
    print(f"📍 Host: {args.host}")
    print(f"📍 Port: {args.port}")
    print(f"🔄 Reload: {'Enabled (Development Mode)' if args.reload else 'Disabled'}")
    print(f"👷 Workers: {args.workers}")
    print(f"📋 Log Level: {args.log_level.upper()}")
    print("=" * 80)
    print()
    print("📚 API Documentation:")
    print(f"  - Swagger UI: http://{args.host}:{args.port}/api/docs")
    print(f"  - ReDoc: http://{args.host}:{args.port}/api/redoc")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 80)
    print()
    
    try:
        import uvicorn
        
        uvicorn.run(
            "voice_cloning.api:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers if not args.reload else 1,
            log_level=args.log_level,
        )
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped by user")
    except ImportError as e:
        print(f"❌ Missing dependency: {str(e)}")
        print("\nPlease install required packages:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error starting server: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
