import subprocess

# Run the script and redirect input from input.txt
subprocess.run(["python", "main.py"], stdin=open("input.txt", "r"))