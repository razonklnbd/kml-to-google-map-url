import os
import time

UPLOAD_DIR = "/app/uploads"
LOG_DIR = "/app/logs"

UPLOAD_MAX_AGE = 60 * 30   # 30 minutes
LOG_MAX_AGE = 60 * 60 * 24 # 24 hours


def cleanup_folder(folder, max_age):
    now = time.time()

    if not os.path.exists(folder):
        return

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if not os.path.isfile(path):
            continue

        if now - os.path.getmtime(path) > max_age:
            try:
                os.remove(path)
                print(f"[CLEANUP] Deleted {path}")
            except Exception as e:
                print(f"[CLEANUP ERROR] {e}")


def run():
    print("[WORKER] Cleanup worker started")

    while True:

        cleanup_folder(UPLOAD_DIR, UPLOAD_MAX_AGE)
        cleanup_folder(LOG_DIR, LOG_MAX_AGE)

        time.sleep(60)  # run every minute


if __name__ == "__main__":
    run()