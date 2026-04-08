"""TriageFlow Server — OpenEnv multi-mode deployment entry point.

This module re-exports the FastAPI app from the root app.py and provides
a main() entry point for the [project.scripts] console script.
"""

import sys
import os

# Ensure the project root is on sys.path so root-level modules resolve
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from app import app  # noqa: E402  — re-export the FastAPI instance


def main():
    """Console-script entry point: ``triageflow-server``."""
    import uvicorn
    uvicorn.run(
        "server.app:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "7860")),
    )


if __name__ == "__main__":
    main()
