#!/usr/bin/env python3
"""Capital Manifold Web Server Runner.

Launches the production FastAPI application via Uvicorn on 127.0.0.1:8765.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import uvicorn


def main() -> None:
    parser = argparse.ArgumentParser(description="Capital Manifold Financial Web Application Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765, help="Port to listen on (default: 8765)")
    parser.add_argument("--reload", action="store_true", help="Enable live auto-reload for development")
    args = parser.parse_args()

    print("=" * 80)
    print("  CAPITAL MANIFOLD: INSTITUTIONAL FINANCIAL ENGINEERING DASHBOARD")
    print(f"  Access URL: http://{args.host}:{args.port}")
    print("  API Docs:   http://{args.host}:{args.port}/docs")
    print("=" * 80)

    uvicorn.run(
        "capital_manifold.web.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
