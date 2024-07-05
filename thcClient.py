import subprocess
import os

def startServer():
    # Change the working directory
    os.chdir(r"C:\xampp\htdocs\ok\thc\THC\thc-master\thc\demo\evoting")
    
    # Define the command to run
    command = ["python3", "-m", "thc.demo.evoting.client", "--new", "127.0.0.1:9380"]
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing the command: {e}")

if __name__ == '__main__':
    startServer()
