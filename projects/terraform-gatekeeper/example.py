import subprocess
result = subprocess.run(["echo", "hello"], capture_output=True)
print(dir(result)) # This will show 'stdout', 'stderr', etc.
print(result.stdout)