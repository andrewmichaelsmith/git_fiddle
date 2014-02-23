import sys
import subprocess
import logging
import git_repo_create_main
import os

from config import (
    FILE_LIST,
    REMOTE,
    BRANCH_NAME,
)


def run():
    init()

    contents = ":-)"

    worked = []
    failed = []

    for f in FILE_LIST:
        repo_loc    = git_repo_create_main.create_repo(f, contents)
        push_worked = git_push(repo_loc)

        if push_worked:
            worked.append(f)
        else:
            failed.append(f)

    logging.info("%d failed. %d worked", len(failed), len(worked))
    logging.info("failed: %s", ",".join(failed))
    logging.info("worked: %s", ",".join(worked))


def git_push(loc):

    branch_name = BRANCH_NAME or os.path.basename(loc)

    logging.info("Trying to push %s", loc)

    p = subprocess.Popen(['git', 'remote', 'add', 'origin', REMOTE], cwd=loc)
    p.wait()

    p = subprocess.Popen(['git', 'checkout', '-b', branch_name], cwd=loc)
    p.wait()

    p = subprocess.Popen(['git', 'pull', 'origin', branch_name])
    p.wait()

    p = subprocess.Popen(['git', 'push', '-u', 'origin', branch_name], cwd=loc)
    code = p.wait()

    return code == 0

def init():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


if __name__ == "__main__":
    run()

