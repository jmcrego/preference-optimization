"""Report the effective scratch setting without probing the cluster."""

from scratch_paths import scratch_dir

if __name__ == "__main__":
    try:
        print(scratch_dir())
    except ValueError as error:
        raise SystemExit(str(error)) from error
