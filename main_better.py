import sys
import logging
import subprocess
import tempfile
import binascii
import os

from hashlib import (
    sha1,
)

def run():
    init()

    loc = create_tmp_dir()
    git_init(loc)

    #make_object_dir(loc)

    blob   = create_blob("blah!")
    tree   = create_tree(blob, "..")
    commit = create_commit(tree)

    for f in [blob, tree, commit]:
        write(loc, f)

    set_head(loc, commit)

def make_object_dir(loc):
    os.makedirs("%s/.git/objects")

def write(loc, contents):
    sha_hash = get_hash(contents)

    obj_dir = "%s/.git/objects/%s" % (loc, sha_hash[:2])

    if not os.path.exists(obj_dir):
        os.makedirs(obj_dir)

    with open('%s/.git/objects/%s/%s' % (loc, sha_hash[:2], sha_hash[2:]), 'w+') as f:
        logging.info("Writing %s", contents)
        f.write(contents)

def set_head(loc, head):

    sha_hash = get_hash(head)
    with open('%s/.git/refs/heads/master' % loc, 'w+') as f:
        f.write(sha_hash)

def init():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

def create_blob(contents):
    #'blob 13\x00test content\n'
    return "blob %d\x00%s" % (len(contents), contents)

def create_tree(blob, file_name):

    blob_sha1 = get_hash(blob)

    mode = '100644'
    byte_sha1 = binascii.unhexlify(blob_sha1)
    tree_base = "%s %s\x00%s" % (mode, file_name, blob_sha1)
    return "tree %d\x00%s" % (len(tree_base), tree_base)

def create_commit(tree):

    tree_hash = get_hash(tree)

    #commit 153\x00tree 80865964295ae2f11d27383e5f9c0b58a8ef21da\nauthor Woop <woop@woop.com> 1392929224 +0000\ncommitter Woop <woop@woop.com> 1392929224 +0000\n\nfirst commit\n
    author_line     = "author Woop <woop@woop.com> 1392929224 +0000"
    committer_line  = "committer Woop <woop@woop.com> 1392929224 +0000"
    commit_msg      = "first commit"

    commit_base = "tree %s\n%s\n%s\n\n%s\n" % (tree_hash, author_line, committer_line, commit_msg)
    return "commit %d\x00%s" % (len(commit_base), commit_base)

def create_tmp_dir():
    loc = tempfile.mkdtemp()
    logging.info("Created %s", loc)
    return loc

def git_init(loc):
    p = subprocess.Popen(['git', 'init'], cwd=loc)
    p.wait()

def get_hash(contents):
    return sha1(contents).hexdigest()

if __name__ ==  "__main__":
    run()

