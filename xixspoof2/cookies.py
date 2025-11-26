import os
COOKIE_FILE = "cookie.txt"

def load_cookie(arg_cookie: str | None) -> str | None:
    if arg_cookie:
        return arg_cookie.strip()
    env = os.getenv("RBLX_COOKIE")
    if env:
        return env.strip()
    if os.path.isfile(COOKIE_FILE):
        try:
            with open(COOKIE_FILE, "r", encoding="utf-8") as f:
                txt = f.read().strip()
                if txt:
                    return txt
        except Exception:
            pass
    return None

def save_cookie(cookie: str):
    try:
        with open(COOKIE_FILE, "w", encoding="utf-8") as f:
            f.write(cookie.strip())
    except Exception:
        pass
