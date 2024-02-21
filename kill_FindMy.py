#!/usr/bin/python3
import subprocess
import time

def kill_findmy():
    try:
        result = subprocess.run(["pgrep", "FindMy"], capture_output=True, text=True, check=True)
        pids = result.stdout.splitlines()
        for pid in pids:
            subprocess.run(["kill", pid])
            print(f"FindMy application with PID {pid} killed successfully")
    except subprocess.CalledProcessError:
        print("Error: FindMy application not found or unable to be killed")

if __name__ == "__main__":
    time.sleep(10)
    kill_findmy()
