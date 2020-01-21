import subprocess
import os

current_dir = os.getcwd()
#working_dir = current_dir + r'\Audiveris\bin'
working_dir = r'C:\Program Files\Audiveris\bin'
print(working_dir)

process = subprocess.check_call(["Audiveris", "-batch", "-export", f"Pi.pdf"], shell=True, cwd=working_dir)
print("done")