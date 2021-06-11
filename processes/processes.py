import subprocess
import sys


def spawn_test():
    """Examples of spawning subprocesses"""

    # Spawn subprocess, tell it to execute command
    subprocess.run([sys.executable, "-c",
                    "print('Greetings form a ""subprocess')"])

    # Spawn subprocess in intermediate shell, tell it to run command
    # I.e. all shell features in command string processed first
    subprocess.run('node --version', shell=True)


# Example simple bash command execution
def _copy_file():
    output = subprocess.run(['ls'], check=True, stdout=subprocess.PIPE,
                            universal_newlines=True)
    if output.stderr is not None:
        print("Failed to read execute command")
    else:
        print(output.stdout)


spawn_test()
_copy_file()
