import logging
import tempfile
import os
import sys

from git import (
    Repo,
)
def run():

    init()

    base_repo = "%s/base/" % os.path.dirname(os.path.realpath(__file__))
    base_repo = Repo.clone(base_repo)

    import pdb; pdb.set_trace()

    repo = create_repo(base_repo)

def create_repo(base_repo):
    loc = create_tmp_dir()
    return base_repo.clone(loc)

def init():

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

def create_tmp_dir():
    loc = tempfile.mkdtemp()
    logging.info("Created %s", loc)
    return loc

if __name__ == "__main__":
    run()
