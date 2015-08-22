svyn
====

svyn is an svn helper. It allows you to specify some typical repository
information in a config file and simplifies several common commands based on
that information. If you typically branch from a shared trunk, or operate on
several different repositories and would like a couple shortcuts, svyn might
be for you. Right now branching and listing/searching branches, as well as
release tagging are the entirety of its powers.
Future features may include support for file history
information and repository introspection.

Installation
------------
Sadly, `pysvn` is a terrible dependency to have. I am omitting it as it
cannot be automatically supplied due to a host of platform and SVN version
issues. You will need to get it wherever you want to use `svyn` yourself.

.svynrc
-------

The .svynrc file is in .ini format. It can handle multiple sections. Each section should specify
four variables:
* ``repo_url``: However you want to represent the base URL for your repo
* ``root_dir``: What you think of as the root dir of your repo
* ``branches_dir``: The path to where your branches are stored.
* ``copy_source_dir``: The source directory from which branches will be copied.
* ``release_dir``: The directory where numbered releases are stored

The ``branches``, ``copy_source_dir``, ``release_dir`` should be relative to the
``root_dir``. The ``root_dir`` is essentially concatenated with the ``repo_url`` and
then with one of the prior variables to generate the full address for svn.

Example conf section
--------------------

::

    [default]
    repo_url = svn+ssh://svn/svnroot
    root_dir = some/project/source
    branches_dir = branches
    copy_source_dir = trunk

In this case, ``svyn branch foo`` would use
``svn+ssh://svn/svnroot/some/project/source/trunk`` as the source for new
branches, which it would then copy to ``svn+ssh://svn/svnroot/some/project/source/branches/foo``

The section to be searched for the variables can be set for any svyn command
with the ``-c`` flag, so ``svyn -c bar_section branch`` would then use variables
from ``[bar_section]`` in the ``.svynrc`` file.

Commands
--------

See `svyn -h` and `svyn {command} -h` for quick help

* branch: Copies head of trunk to a branc, named by the command arg.
* list: Lists current branches, -s to search -m for current user is last committer.
* release: Copies specified trunk rev to release dir. Will auto-calculate release
  number or can be overridden.
