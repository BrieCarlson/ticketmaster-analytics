import subprocess
import sys


def run_step(script):
    print(f"\n{'=' * 60}")
    print(f"Running {script}")
    print(f"{'=' * 60}")

    result = subprocess.run(
        [sys.executable, script],
        check=True,
    )

    return result.returncode


def main():
    scripts = [
        "src/fetch_events.py",
        "src/transform.py",
        "src/load_database.py",
    ]

    for script in scripts:
        run_step(script)

    print(f"\n{'=' * 60}")
    print("PIPELINE COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()