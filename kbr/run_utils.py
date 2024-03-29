import subprocess

import sys
import os


class ExecutionInfo:
    def __init__(self, p_status: int, stdout: str, stderr: str):
        self.p_status = p_status
        self.stdout = stdout
        self.stderr = stderr


def exit_fail(msg: str = "") -> None:
    print(msg)
    sys.exit(-1)


def exit_ok(msg: str = "") -> None:
    print(msg)
    sys.exit(0)


def launch_cmd(cmd: str, cwd: str = "", use_shell_env:bool=False) -> ExecutionInfo:
    effective_command = cmd

    d = None
    if use_shell_env:
        d = dict(os.environ)


    if cwd == '':
        p = subprocess.Popen(effective_command, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE, env=d)
    else:
        p = subprocess.Popen(effective_command, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE, cwd=cwd, env=d)

    stdout, stderr = p.communicate()
    p_status = p.wait()
    return ExecutionInfo(p_status, stdout, stderr)

def print_outputs(e:ExecutionInfo) -> None:
    if e.stdout != b'':
        print(e.stdout.decode('utf-8').rstrip("\n"))

    if e.stderr != b'':
        print(e.stderr.decode('utf-8').rstrip("\n"))

