import sys

def render_bar(done: int, total: int, width: int = 40) -> str:
    total = max(total, 1)
    ratio = done / total
    filled = int(width * ratio)
    return "[" + "#" * filled + "-" * (width - filled) + f"] {done}/{total} ({ratio*100:5.1f}%)"

def update_progress(done: int, total: int, prefix="Uploading"):
    sys.stdout.write("\r" + prefix + " " + render_bar(done, total))
    sys.stdout.flush()

def finish_progress(total: int, prefix="Uploading"):
    update_progress(total, total, prefix)
    sys.stdout.write("\n")
    sys.stdout.flush()
