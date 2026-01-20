import subprocess
import datetime

def idle_seconds(seat="seat0"):
    try:
        result = subprocess.run(
            [
                "loginctl",
                "show-seat",
                seat,
                "-p",
                "IdleSinceHint",
                "--value",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        idle_since_str = result.stdout.strip()
        if not idle_since_str:
            raise RuntimeError("IdleSinceHint is empty")

        # Parse systemd timestamp: "2026-01-16 08:42:31 CST"
        idle_since = datetime.datetime.strptime(
            idle_since_str, "%Y-%m-%d %H:%M:%S %Z"
        )

        now = datetime.datetime.now(tz=idle_since.tzinfo)
        delta = now - idle_since

        return delta.total_seconds()

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"loginctl failed: {e.stderr}") from e

    except Exception as e:
        raise RuntimeError(f"Failed to determine idle time: {e}") from e

def idle_minutes():
    return idle_seconds() / 60  # minutes