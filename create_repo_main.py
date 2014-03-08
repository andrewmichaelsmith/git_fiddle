import logging
import sys

from git_obj import (
    Blob,
    Tree,
    Commit,
    Repo,
    Remote,
)

def run():
    init()
    basic_repo()
    #one_level_repo()
    #multiple_commits()
    #basic_repo_push()
    #submodule()


def submodule():

    repo = Repo()

    commit_1 = Commit(None, Tree([Blob(body="xx", name="boogalooo")]))

    repo.add_remote(Remote("blah", "bloo", "git://github.com/chneukirchen/rack.git"))

    repo.set_head(commit_1)


    repo.git_push()


def multiple_commits():

    commit_1 = Commit(None, Tree([Blob(body="xx", name="..")]))
    commit_2 = Commit(commit_1, Tree([Blob(body="yy", name="HO")]))

    repo = Repo()
    repo.set_head(commit_2)

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
    blobs.append(Blob(body="hi", name=".."))

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


