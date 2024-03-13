
import kbr.run_utils as run_utils


def commit(msg:str, filename:str=None) -> None:

    cmd = f'git commit -m"{msg}"'
    if filename is not None:
        cmd += f" {filename}"

    cmd_res = run_utils.launch_cmd(cmd)
    run_utils.print_outputs( cmd_res )

def push() -> None:

    cmd = f"git push"
    cmd_res = run_utils.launch_cmd(cmd)
    run_utils.print_outputs( cmd_res )


def commit_and_push(msg:str, filename:str=None) -> None:
    commit(msg, filename)
    push()

def tag():
    pass



def unbumped():
    res = run_utils.launch_cmd(cmd='git log --pretty=format:"%ar, %s"')
    stdout = res.stdout.decode("utf-8")
    print("Commits since last bump")
    print("=======================")
    for l in stdout.split("\n"):
        if "version bump" in l:
            break
        print(l)
    print("")

def bump_history(limit=10):
    res = run_utils.launch_cmd(cmd='git log --pretty=format:"%h: %ar, %s"')
    stdout = res.stdout.decode("utf-8")
    print("Bump history")
    print("=======================")
    for l in stdout.split("\n"):
        if "version bump" in l:
            print(l)
            limit -=  1
        
        if limit == 0:
            break
    print("")
