import logging
import tempfile
import os
import sys
import tarfile
import argparse
import hashlib
import shutil
import zlib

ROOT             = os.path.dirname(os.path.realpath(__file__))

BASE_REPO_TAR_GZ = "%s/%s" % (ROOT, "pre-made-repo.tar.gz")
#This describes the contents of BASE_REPO_TAR_GZ
TREE_HASH        = "775a99b79ec5fbdca77d58ca69db102ba9f42098"
FILE_NAME        = "aaaaa"

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
    repo_dir = create_new_base_repo()

    obj_dir = "%s/.git/objects" % repo_dir

    tree_file = "%s/%s/%s" % (obj_dir, TREE_HASH[:2], TREE_HASH[2:])

    with open(tree_file, 'r+') as f:
        raw = f.read()

        blob = zlib.decompress(raw)
        blob = blob.replace(FILE_NAME, file_name)

        f.seek(0)
        f.write(zlib.compress(blob))
        f.truncate()


    new_hash = hashlib.sha1(blob).hexdigest()

    new_tree_dir =  "%s/%s/" % (obj_dir, new_hash[:2])

    if not os.path.exists(new_tree_dir):
        os.makedirs(new_tree_dir)

    new_tree_file = "%s/%s" % (new_tree_dir, new_hash[2:])

    shutil.move(tree_file, new_tree_file)


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
