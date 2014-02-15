import logging
import tempfile
import os
import sys
import tarfile

from git import (
    Repo,
)

ROOT             = os.path.dirname(os.path.realpath(__file__))
BASE_REPO_TAR_GZ = "%s/%s" % (ROOT, "base-repo.tar.gz")

def run():

    init()

    repo_dir = create_new_base_repo()

def create_new_base_repo():
    base_tar = tarfile.open(BASE_REPO_TAR_GZ)
    tmp = create_tmp_dir()

    base_tar.extractall(path=tmp)

    logging.info("Created base repo at %s", tmp)

    return tmp

def init():

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

def create_tmp_dir():
    loc = tempfile.mkdtemp()
    logging.info("Created %s", loc)
    return loc

if __name__ == "__main__":
    run()
