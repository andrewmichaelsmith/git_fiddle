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
    #basic_repo()
    #one_level_repo()
    multiple_commits()


def multiple_commits():

    commit_1 = Commit(None, Tree([Blob(body="xx", name="HI")]))
    commit_2 = Commit(commit_1, Tree([Blob(body="yy", name="HO")]))

    repo = Repo()
    repo.set_head(commit_2)

    #Andy Todo

    repo.write()

def one_level_repo():

    tree_a = Tree([Blob(body="xx", name="boo")], name="boogaloo")
    tree_b = Tree([tree_a])

    commit = Commit(None, tree_b)

    repo = Repo()
    repo.set_head(commit)
    repo.write()

def basic_repo():

    blobs = []
    for x in xrange(100):
        blobs.append(Blob(body="hi", name="..%s" % x))

    tree = Tree(blobs)
    commit = Commit(None,tree)

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
    def __init__(self, body, name, mode='100644'):
        self.body = body
        self.mode = mode
        self.name = name

    def __str__(self):
        return "blob %d\x00%s" % (len(self.body), self.body)

class Tree(GitObject):
    """
        A tree object
    """
    def __init__(self, children, mode='0040000', name=None):
        self.children = children
        self.mode = mode
        self.name = name

    def __str__(self):
        tree_base = ""

        for child in self.children:
            tree_base += "%s %s\x00%s" % \
                    (child.mode, child.name, child.get_byte_hash())

        return "tree %d\x00%s" % (len(tree_base), tree_base)


class Commit(GitObject):
    """
        A commit object. We don't do parents yet.
    """
    def __init__(self, parent, tree, username=USERNAME, email=EMAIL, author_time=AUTHOR_TIMESTAMP, committer_time=COMMITTER_TIMESTAMP, commit_msg="first commit"):
        self.tree = tree
        self.author_line = "author %s <%s> %s +0000" % \
                (username, email, author_time)
        self.committer_line = "committer %s <%s> %s +0000" % \
                (username, email, committer_time)
        self.commit_msg = commit_msg
        self.parent = parent
        if parent:
            self.parent_line = "parent %s\n" % parent.get_hash()
        else:
            self.parent_line = ""

    def __str__(self):
        commit_base = "tree %s\n%s%s\n%s\n\n%s\n" % \
                (self.tree.get_hash(), self.parent_line, self.author_line, self.committer_line, self.commit_msg)
        return "commit %d\x00%s" % (len(commit_base), commit_base)

class Repo(object):


    def __init__(self, dir=None):

        self.dir = dir or self.create_tmp_dir()

        self.git_init()

        self.commits = set()
        self.head = None

    def create_tmp_dir(self):
        loc = tempfile.mkdtemp()
        logging.info("Created %s", loc)
        return loc

    def set_head(self, commit):
        self.head = commit

    def write(self):
        self.write_commit(self.head)

    def write_commit(self, commit):
        self.write_all(commit.tree)

        commit.tree.write(self.dir)

        commit.write(self.dir)

        if commit.parent:
            self.write_commit(commit.parent)

        if self.head:
            with open('%s/.git/refs/heads/master' % self.dir, 'w+') as f:
                f.write(self.head.get_hash())

    def write_all(self, parent):
      for child in parent.children:
          child.write(self.dir)

          if hasattr(child, 'children'):
              self.write_all(child)


    def git_init(self):
        proc = subprocess.Popen(['git', 'init'], cwd=self.dir)
        proc.wait()

    def git_push(self, remote, branch=None):

        self.branch = branch or self.dir

        logging.info("Trying to push %s", self.branch)

        p = subprocess.Popen(['git', 'remote', 'add', 'origin', remote], cwd=self.dir)
        p.wait()

        p = subprocess.Popen(['git', 'checkout', '-b', branch], cwd=self.dir)
        p.wait()

        p = subprocess.Popen(['git', 'pull', 'origin', branch], cwd=self.dir)
        p.wait()

        p = subprocess.Popen(['git', 'push', '-u', 'origin', branch], cwd=self.dir)
        code = p.wait()

        return code == 0


if __name__ ==  "__main__":
    run()
