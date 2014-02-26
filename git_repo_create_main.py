import sys
import logging
import subprocess
import tempfile
import binascii
import os
import zlib

from hashlib import (
    sha1,
)

from config import (
    USERNAME,
    EMAIL,
    AUTHOR_TIMESTAMP,
    COMMITTER_TIMESTAMP,
)

def run():
    init()
    basic_repo()



#Def create_repo2():
#
#    loc = create_tmp_dir()
#    git_init(loc)
#
#    blob   = create_blob("whaa")
#    tree   = create_tree('100644', get_hash(blob), "hi")
#    tree2  = create_tree('40000', get_hash(tree), "..")
#    commit = create_commit(tree2)
#
#    for f in [blob, tree, commit]:
#        write(loc, f)
#
#    set_head(loc, commit)
#
#    return loc
#
#
#def create_repo(mode, file_name, file_contents):
#
#    loc = create_tmp_dir()
#    git_init(loc)
#
#    blob   = create_blob(file_contents)
#    tree   = create_tree(mode, get_hash(blob), file_name)
#    commit = create_commit(tree)
#
#    for f in [blob, tree, commit]:
#        write(loc, f)
#
#    set_head(loc, commit)
#
#    return loc

def basic_repo():

    blob = Blob(body="hi", file_name="..")
    tree = Tree([blob])
    commit = Commit(tree)

    repo = Repo()
    repo.set_head(commit)
    repo.write()



def init():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class GitObject(object):
    def write(self, repo_loc):
        sha_hash = self.get_hash()

        obj_dir = "%s/.git/objects/%s" % (repo_loc, sha_hash[:2])

        if not os.path.exists(obj_dir):
            os.makedirs(obj_dir)

        with open('%s/.git/objects/%s/%s' % (repo_loc, sha_hash[:2], sha_hash[2:]), 'w+') as f:
            logging.debug("Writing %s", str(self))
            f.write(zlib.compress(str(self)))


    def get_hash(self):
        return sha1(str(self)).hexdigest()

    def get_byte_hash(self):
        return binascii.unhexlify(self.get_hash())

class Blob(GitObject):
    def __init__(self, body, file_name, mode='100644'):
        self.body = body
        self.mode = mode
        self.file_name = file_name

    def __str__(self):
        #'blob 13\x00test content\n'
        return "blob %d\x00%s" % (len(self.body), self.body)

class Tree(GitObject):
    """
        A tree object
    """
    def __init__(self, children, mode='0040000'):
        self.children = children
        self.mode = mode

    def __str__(self):
        #'tree 29\x00100644 a\x00\xe6\x9d\xe2\x9b\xb2\xd1\xd6CK\x8b)\xaewZ\xd8\xc2\xe4\x8cS\x91'
        #or
        #'tree 174\x00100644 a\x00\xe6\x9d\xe2\x9b\xb2\xd1\xd6CK\x8b)\xaewZ\xd8\xc2\xe4\x8cS\x91100644 b\x00\xe6\x9d\xe2\x9b\xb2\xd1\xd6CK\x8b)\xaewZ\xd8\xc2\xe4\x8cS\x91100644 c\x00\xe6\x9d\xe2\x9b\xb2\xd1\xd6CK\x8b)\xaewZ\xd8\xc2\xe4\x8cS\x91100644 d\x00\xe6\x9d\xe2\x9b\xb2\xd1\xd6CK\x8b)\xaewZ\xd8\xc2\xe4\x8cS\x91100644 e\x00\xe6\x9d\xe2\x9b\xb2\xd1\xd6CK\x8b)\xaewZ\xd8\xc2\xe4\x8cS\x91100644 f\x00\xe6\x9d\xe2\x9b\xb2\xd1\xd6CK\x8b)\xaewZ\xd8\xc2\xe4\x8cS\x91'

        tree_base = ""

        for child in self.children:
            tree_base += "%s %s\x00%s" % \
                    (child.mode, child.file_name, child.get_byte_hash())

        return "tree %d\x00%s" % (len(tree_base), tree_base)


class Commit(GitObject):
    """
        A commit object. We don't do parents yet.
    """
    def __init__(self, tree, username=USERNAME, email=EMAIL, author_time=AUTHOR_TIMESTAMP, committer_time=COMMITTER_TIMESTAMP, commit_msg="first commit"):
        self.tree = tree
        self.author_line = "author %s <%s> %s +0000" % \
                (username, email, author_time)
        self.committer_line = "committer %s <%s> %s +0000" % \
                (username, email, committer_time)
        self.commit_msg = commit_msg

    def __str__(self):
        commit_base = "tree %s\n%s\n%s\n\n%s\n" % \
                (self.tree.get_hash(), self.author_line, self.committer_line, self.commit_msg)
        return "commit %d\x00%s" % (len(commit_base), commit_base)

class Repo(object):


    def __init__(self, dir=None):
        if not dir:
            self.dir = self.create_tmp_dir()
        else:
            self.dir = dir

        self.git_init()

        self.commits = set()
        self.head = None

    def create_tmp_dir(self):
        loc = tempfile.mkdtemp()
        logging.info("Created %s", loc)
        return loc

    def git_init(self):
        proc = subprocess.Popen(['git', 'init'], cwd=self.dir)
        proc.wait()

    def set_head(self, commit):

        self.head = commit
        self.commits.add(commit)

    def add_commit(self, commit):
        self.commits.add(commit)

    def write(self):

        for commit in self.commits:

            for child in commit.tree.children:
                child.write(self.dir)

            commit.tree.write(self.dir)
            commit.write(self.dir)


        if self.head:
            with open('%s/.git/refs/heads/master' % self.dir, 'w+') as f:
                f.write(self.head.get_hash())


if __name__ ==  "__main__":
    run()

