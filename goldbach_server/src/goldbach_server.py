import server as Server
import cpu_usage.api as Api
from multiprocessing import Pool
from time import sleep

def serverKiller(pool):
  try:
    while True: sleep(99999)
  except KeyboardInterrupt:
    print("[Goldbach Server] Shutting down")
    pool.close()
    pool.terminate()
    pool.join()

if __name__ == "__main__":
  print("[Goldbach Server] Starting")
  pool = Pool(processes=2)
  pool.apply_async(Server.start)
  pool.apply_async(Api.start)
  serverKiller(pool)