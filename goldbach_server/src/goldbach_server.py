import server as Server
import cpu_usage.api as Api
import multiprocessing
import signal
import time

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def serverKiller():
  try:
    while True: time.sleep(99999)
  except KeyboardInterrupt:
    print("[\nGoldbach Server] Shutting down")

if __name__ == "__main__":
    print("\n[Goldbach Server] Starting")
    pool = multiprocessing.Pool(2, init_worker)
    pool.apply_async(Server.start)
    pool.apply_async(Api.start)
    serverKiller()
    pool.terminate()
    pool.join()