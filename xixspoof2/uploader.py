# xixspoof2/uploader.py
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, random
from .logutil import info, warn
from .roblox import RobloxAPI

def upload_all(cookie, ids, group, threads):
    api = RobloxAPI(cookie)
    id_map = {}
    errors = []

    # Gentle pacing between tasks to avoid rate limits / TLS EOFs
    def do(old):
        # jitter between downloads to spread load
        time.sleep(random.uniform(0.05, 0.2))
        data = api.dl(old)
        # jitter before upload as well
        time.sleep(random.uniform(0.1, 0.3))
        nid = api.upload(data, f"Clone_{old}", "Uploaded via xixspoof2", group)
        return old, nid

    total = len(ids)
    info(f"Re-uploading {total} animation(s)… (threads={threads})")

    # Keep parallelism low; API is picky. 2–3 is safest.
    threads = max(1, min(threads, 3))

    with ThreadPoolExecutor(max_workers=threads) as ex:
        futs = {ex.submit(do, oid): oid for oid in ids}
        done = 0
        for fut in as_completed(futs):
            done += 1
            old = futs[fut]
            try:
                o, n = fut.result()
                id_map[o] = n
                info(f"[{done}/{total}] {o} -> {n}")
            except Exception as e:
                warn(f"[{done}/{total}] {old} FAILED: {e}")
                errors.append((old, str(e)))
                # brief pause after a failure to ease pressure
                time.sleep(0.5)

    return id_map, errors
