

"""svyn.svyn: provides entry point main()."""


__version__ = "0.8.0"

from .svynworker import SvynWorker, SvynError

# Standard library
import argparse
import ConfigParser
import os
import sys


MESSAGE_MISSING_CONFIG = "Config file expected at ~/.svynrc not found."
MESSAGE_UNABLE_TO_SWITCH = "Unable to switch: {}"
SVYN_CONF = "~/.svyn.conf"


def init_optparser():
    p = argparse.ArgumentParser(
        description="Convenience wrapper for svn functions.")
    p.add_argument("--version", action="version", version="0.1.0")
    p.add_argument(
        "--config",
        "-c",
        default="default",
        help="Config section to use for repo paths."
    )

    subs = p.add_subparsers(title="commands")

    branch_p = subs.add_parser(
        "branch",
        help="Create svn cp of copy_target to branches/<NAME> with default "
             "message."
    )
    branch_p.add_argument(
        "-s",
        "--switch",
        help="Switch working directory to new branch.",
        action="store_true",
        default=False
    )
    branch_p.add_argument(
        "-m",
        "--message",
        help="Add an additional message describing branch."
    )
    branch_p.add_argument(
        "name",
        help="Intended name of new branch."
    )
    branch_p.set_defaults(func=branch)

    list_p = subs.add_parser(
        "list",
        help="Lists current branches. Optionally search in them with -s"
    )
    list_p.add_argument(
        "-s",
        "--search",
        help="String to search directory names for."
    )
    list_p.add_argument(
        "-m",
        "--mine",
        action="store_true",
        default=False,
        help="Filter listed branches to those where current user is "
             "last author."
    )
    list_p.set_defaults(func=list)

    release_p = subs.add_parser(
        "release",
        help="Copy specified source revision to release directory. Will"
        " automatically calculate release name based on specified type."
    )
    release_p.add_argument(
        "-n",
        "--name",
        help="Overrides calculated release name."
    )
    release_p.add_argument(
        "-f",
        "--force",
        help="Skip confirmations; JUST DO IT."
    )
    release_p.add_argument(
        "revision",
        help="Revision of source to use for release."
    )
    release_p.add_argument(
        "type",
        choices=["major", "minor", "point"],
        help="Type of release to tag."
    )
    release_p.set_defaults(func=release)

    return p


def init_config():
    """Expects a .svynrc in home folder."""
    cp = ConfigParser.SafeConfigParser()
    try:
        with open(os.path.expanduser(SVYN_CONF)) as config:
            cp.readfp(config)
    except IOError:
        print MESSAGE_MISSING_CONFIG
        sys.exit(1)
    return cp


def main():
    p = init_optparser()
    c = init_config()
    args = p.parse_args()
    s = SvynWorker(dict(c.items(args.config)))
    # Execute command with options and arguments.
    args.func(s, args)


def branch(s, args):
    branch = s.branch(args.name, args.message)
    if args.switch:
        try:
            s.switch(os.getcwd(), branch)
        except SvynError as e:
            print MESSAGE_UNABLE_TO_SWITCH.format(repr(e))
            sys.exit(1)


def list(s, args):
    branches = s.list(args.search, args.mine)
    for b in branches:
        print b


def release(s, args):
    name = args.name if args.name else s.get_next_release(args.type)
    if not args.force:
        message = ("About to release `{}' at revision `{}' to location: `{}'."
                   " Proceed? [y/n]")
        message.format(s.get_copy_path(), args.revision,
                       s.get_release_path(name))
        res = raw_input(message)
        if not res.tolower() == "y":
            print "Aborting."
            sys.exit(0)

    s.release(args.revision, name)
