"""Command-line entry point for parallel TSV conversion."""

from pathlib import Path
import sys

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from preference_optimization.data.parallel_tsv import main

    main()
