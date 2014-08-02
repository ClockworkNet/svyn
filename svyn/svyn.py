

"""svyn.svyn: provides entry point main()."""


__version__ = "0.1.0"

import argparse
import ConfigParser
import os
import pysvn
import sys

MESSAGE_MISSING_CONFIG = "Config file expected at ~/.svynrc not found."


def branch(s, args):
    s.branch(args.name, args.message)


def init_optparser():
    p = argparse.ArgumentParser(
        description="Convenience wrapper for svn functions.")
    p.add_argument("--version", action="version", version='0.1.0')

    subs = p.add_subparsers()

    branch_p = subs.add_parser(
        "branch",
        help="Create svn cp of copy_target to branches/<NAME>"
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
    branch_p.add_argument("name")
    branch_p.set_defaults(func=branch)

    return p


def init_config():
    """Expects a .svynrc in home folder."""
    cp = ConfigParser.SafeConfigParser()
    try:
        with open(os.path.expanduser("~/.svynrc")) as config:
            cp.readfp(config)
    except IOError:
        print MESSAGE_MISSING_CONFIG
        sys.exit(1)
    return cp


def main():
    c = init_config()
    p = init_optparser()
    args = p.parse_args()
    s = Svyn(dict(c.items("svn")))
    # Execute command with options and arguments.
    args.func(s, args)


class Svyn(object):
    """Mediates pysvn calls in a nice api. I hope."""

    def __init__(self, cnf, client=None):
        if client is None:
            client = pysvn.Client()
        self.client = client
        self.root = cnf['repo_root_dir']
        self.copy_target = cnf['copy_target_dir']
        self.branches = cnf['branches_dir']

        self.client.callback_get_log_message = self.get_log_message

    def branch(self, name, extra_message=None):
        """Copy an origin branch to a target specified by name."""
        message = "Branched: " + name
        if extra_message:
            message += os.linesep + extra_message
        self.message = message

        branch_path = self.get_branch_path(name)
        copy_path = self.get_copy_path()

        self.client.copy(copy_path, branch_path)

    def find_branch(self, search):
        """Searches a list of branches in branch_dir for input string."""
        pass

    def get_log_message(self):
        return self.message

    def get_branch_path(self, name):
        return os.path.join(self.root, self.branches, name)

    def get_copy_path(self):
        return os.path.join(self.root, self.copy_target)
