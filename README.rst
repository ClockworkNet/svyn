svyn
====

svyn is an svn helper. It allows you to specify some typical repository
information in a config file, or use an established convention, and
simplifies several common commands based on that information.
If you typically branch from a shared trunk, or operate on
several different repositories and would like a couple shortcuts, svyn might
be for you. Right now branching and listing/searching branches, as well as
release tagging are the entirety of its powers.
Future features may include support for file history
information and repository introspection.

Installation
------------
Sadly, `pysvn` is a terrible dependency to have. I am omitting from the
setup file as it cannot be automatically installed due to a host of platform and SVN version
issues. You will need to get it wherever you want to use `svyn` yourself.

I recommend `downloading <http://pysvn.tigris.org/project_downloads.html>`_ the appropriate
binaries for your svn and python version. ``svn --version`` and ``python --version`` will
let you know what you need.


Default Behavior
----------------

With no ``.svyn.conf``, svyn will examine the working directory as a working copy.
It will split the path and look for the default ``branches``, ``copy_source`` and
``release`` values (``branches``, ``trunk``, ``tags``) as path parts. It will then try
to determine the working base of your repo and use the defaults for other operations. If
you commonly work on portions of a repo that follow these conventions, you probably won't
need to make a ``.svyn.conf``. If your working directory is not a working copy, svyn
will failover to the ``default`` section of ``.svyn.conf``.

.svyn.conf
----------

The .svyn.conf file contains optional repo information in .ini format. It
is available should your repo naming scheme follow a different convention.
It can handle multiple sections. Each section should specify
three variables:
* ``base``: Fully-qualified path (svn+ssh:// or file:///) to the deepest part of the subtree in which you are interested.
* ``branches``: The path to where your branches are stored.
* ``copy_source``: The source directory from which branches will be copied.
* ``release``: The directory where numbered releases are stored

The ``branches``, ``copy_source``, ``release`` should be relative to the
``base``. The ``base`` is essentially concatenated with the with one of the
other variables to generate the full address for svn.

Example conf section
--------------------

::

    [default]
    base = svn+ssh://svn/svnroot/some/project/source
    branches = splinters
    copy_source = board

In this case, ``svyn branch foo`` would use
``svn+ssh://svn/svnroot/some/project/source/board`` as the source for new
branches, which it would then copy to ``svn+ssh://svn/svnroot/some/project/source/splinters/foo``

The section to be searched for the variables can be set for any svyn command
with the ``-c`` flag, so ``svyn -c bar_section branch`` would then use variables
from ``[bar_section]`` in the ``.svyn.conf`` file.

Commands
--------

See `svyn -h` and `svyn {command} -h` for quick help

* branch: Copies head of trunk to a branc, named by the command arg.
* list: Lists current branches, -s to search -m for current user is last committer.
* release: Copies specified trunk rev to release dir. Will auto-calculate release
  number or can be overridden.
