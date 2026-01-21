import subprocess

def idle_ms():
    out = subprocess.check_output(["xprintidle"], text=True).strip()
    return int(out)  # milliseconds

def idle_seconds():
    return idle_ms() / 1000  # seconds

def idle_minutes():
    return idle_seconds() / 60  # minutes