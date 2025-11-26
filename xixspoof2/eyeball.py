import sys, time, threading

FRAMES = [
    "  .-\"\"-.  \n /  o  o\\ \n|   __   |\n\\  \\__/ /\n '.___.' ",
    "  .-\"\"-.  \n /  o  o\\ \n|   __   |\n\\  ---- /\n '.___.' ",
    "  .-\"\"-.  \n /  o  o\\ \n|   __   |\n\\  \\__/ /\n '.___.' ",
    "  .-\"\"-.  \n /  o  o\\ \n|   __   |\n\\  ---- /\n '.___.' ",
]

def start_eyeball(prefix=\"Scanning for animations…\"):
    stop = threading.Event()
    def run():
        i = 0
        while not stop.is_set():
            frame = FRAMES[i % len(FRAMES)].encode('utf-8').decode('unicode_escape')
            sys.stdout.write("\r" + prefix + "\n" + frame + "\x1b[0K")
            sys.stdout.flush()
            i += 1
            time.sleep(0.15)
        # clear lines
        sys.stdout.write("\r" + " " * 60 + "\n" * 5 + "\r")
        sys.stdout.flush()
    t = threading.Thread(target=run, daemon=True)
    t.start()
    return stop
