## Git Internals



## Goal

Getting the gist of how Git works internally simplifies our mental
model when working with Git repositories.



## Git at its core

* Content-addressable file system
* Plumbing (backend) operations are pretty simple
* Porcelain (frontend) commands just use the plumbing operations
  - many ways to do the same thing -- some shorter, some more
    intuitive



### Git objects

Content-addressable store


### Blob object

Arbitrary data


### Tree object

Listing of sub-objects (blob or tree) with corresponding name and
metadata


### Commit object

Commit metadata:

* tree object
* date
* author
* parent commit(s)
* message


### Tag object

Tag metadata:

* associated object (can be any type, but usually commit)
* tag
* tagger
* message

_(more on this later)_



### Git references

References to commits

Common references:

* HEAD (symbolic ref)
* refs/heads/master
* refs/remotes/origin/master


### Git logs

Logs of changes to references


### Git tags

Special kind of reference (resides in refs/tags)

Types:

* Lightweight (points to a commit object)
* Annotated (points to a tag object)



### Misc

* index (staging)
* interactive
* fast-forward
* merge
* stash



### Some commands

* commit
* checkout
* fetch
* rebase
* cherry-pick



### Exercises

* discard a commit
* import a commit
* recover a commit



#### Reference

[Git Internals](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain)
