import subprocess

import sys


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


def launch_cmd(cmd: str, cwd: str = "") -> ExecutionInfo:
    effective_command = cmd
    p = subprocess.Popen(effective_command, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE,
                         bufsize=1) if cwd == '' else subprocess.Popen(effective_command, stdout=subprocess.PIPE,
                                                                       shell=True, stderr=subprocess.PIPE, bufsize=1,
                                                                       cwd=cwd)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    return ExecutionInfo(p_status, stdout, stderr)
