import logging
import sys

from git_obj import (
    Blob,
    Tree,
    Commit,
    Repo,
)

def run():
    init()
    #basic_repo()
    #one_level_repo()
    #multiple_commits()
    basic_repo_push()


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

def basic_repo_push():

    repo = Repo()
    repo.set_head(Commit(None, Tree([Blob(body="xx", name="boo")])))

    repo.git_push()


def init():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

if __name__ ==  "__main__":
    run()


