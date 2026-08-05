import sys
from pathlib import Path

# Ensure the repository root is on sys.path so test runners find the `app` package.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
