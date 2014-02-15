import logging
import tempfile
import os
import sys
import tarfile
import argparse

from git import (
    Repo,
    IndexEntry,
)

ROOT             = os.path.dirname(os.path.realpath(__file__))
BASE_REPO_TAR_GZ = "%s/%s" % (ROOT, "base-repo.tar.gz")

def run():

    init()

    file_name = get_file_name()

    logging.info("Going to try and create a repo called: %s", file_name)

    create_repo_with_file(file_name)

def get_file_name():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', help='file name to create')

    args = parser.parse_args()

    return args.file_name

def create_repo_with_file(file_name):
    """
        You want a file called "..", we make a git repo
        with a file called "aa".

        We then take the tree that points to "aa" and replace
        it with ".."

        This is quite a hacky way to do this.
    """
    repo_dir = create_new_base_repo()

    repo = Repo(repo_dir)

    fake_file_name = "a" * len(file_name)
    open("%s/%s" % (repo_dir, fake_file_name), 'a').close()

    repo.index.add([fake_file_name])

    file_index = repo.index.entries[(fake_file_name, 0)]

    commit = repo.index.commit("my first commit")

    repo.index.write_tree()


def create_new_base_repo():
    base_tar = tarfile.open(BASE_REPO_TAR_GZ)
    tmp = create_tmp_dir()

    base_tar.extractall(path=tmp)

    logging.info("Created repo at %s", tmp)

    return tmp

def init():

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

def create_tmp_dir():
    loc = tempfile.mkdtemp()
    logging.info("Created %s", loc)
    return loc

if __name__ == "__main__":
    run()
