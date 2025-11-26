from concurrent.futures import ThreadPoolExecutor, as_completed
import time, random
from .logutil import info, warn
from .roblox import RobloxAPI
from .progress import update_progress, finish_progress

def upload_all(cookie, ids, group, threads):
    api = RobloxAPI(cookie)
    id_map = {}
    errors = []

    ids = list(ids)
    total = len(ids)
    info(f"Re-uploading {total} animation(s)… (threads={threads})")

    threads = max(1, min(threads, 3))

    done = 0
    update_progress(done, total)

    def do(old):
        time.sleep(random.uniform(0.05, 0.20))
        data = api.dl(old)
        time.sleep(random.uniform(0.10, 0.30))
        nid = api.upload(data, f"Clone_{old}", "Uploaded via xixspoof2", group)
        return old, nid

    with ThreadPoolExecutor(max_workers=threads) as ex:
        futs = {ex.submit(do, oid): oid for oid in ids}
        for fut in as_completed(futs):
            old = futs[fut]
            try:
                o, n = fut.result()
                id_map[o] = n
            except Exception as e:
                errors.append((old, str(e)))
                warn(f"{old} FAILED: {e}")
            finally:
                done += 1
                update_progress(done, total)

    finish_progress(total)
    return id_map, errors
