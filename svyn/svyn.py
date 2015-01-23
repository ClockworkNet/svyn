

"""svyn.svyn: provides entry point main()."""


__version__ = "0.1.0"

import argparse
import ConfigParser
import os
import pysvn
import sys

MESSAGE_MISSING_CONFIG = "Config file expected at ~/.svynrc not found."


def branch(s, args):
    branch = s.branch(args.name, args.message)
    if args.switch:
        try:
            s.switch(os.getcwd(), branch)
        except SvynError as e:
            print "Unable to switch: %s" % e
            sys.exit(1)


def find(s, args):
    pass


def overlap(s, args):
    pass


def init_optparser():
    p = argparse.ArgumentParser(
        description="Convenience wrapper for svn functions.")
    p.add_argument("--version", action="version", version='0.1.0')

    subs = p.add_subparsers(title="commands")

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
    branch_p.add_argument(
        "name",
        help="Intended name of new branch."
    )
    branch_p.set_defaults(func=branch)

    find_p = subs.add_parser(
        "find",
        help="Searches ls of branch_dir for supplied string"
    )
    find_p.add_argument(
        "search",
        help="String to find."
    )
    find_p.set_defaults(func=find)

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
        self.repo = cnf['repo_url']
        self.root = cnf['root_dir']
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

        return branch_path

    def switch(self, path, repo_url):
        try:
            self.client.switch(path, repo_url)
        except pysvn.ClientError as e:
            self.handle_client_error(e)

    def overlap(self, rev1, rev2):
        """Determines if any files have changed in both revisions."""
        pass

    def accumulate_changed_paths(self, rev1, rev2):
        logs = self.fetch_logs(
            self.get_copy_target_path(),  # Assuming want trunk changes - shady
            start=rev2,
            end=rev1,
        )
        changed_paths = set()
        for l in logs:
            changed_paths.update(p.path for p in l.changed_paths)

        return changed_paths

    def touched(self, rev1, rev2, file):
        """Determines if a file has changed between two revisions."""

    def find_branch(self, search):
        """Searches a list of branches in branch_dir for input string."""
        pass

    def handle_client_error(self, err):
        raise SvynError(str(err))

    def get_branch_first_rev(self, branch):
        """Finds the rev at which a branch was copied."""
        pass

    def get_branch_last_rev(self, branch):
        """Finds the last rev at which a branch existed."""
        logs = self.fetch_logs(
            self.get_branch_path(''),
            paths=True,
            limit=100
        )

        for l in logs:
            for p in l.changed_paths:
                if branch in p.path:
                    return l.revision.num

    def fetch_logs(self, dir, paths=False, start=None, end=None, limit=0):
        if start:
            rev_start = pysvn.Revision(opt_revision_kind.number, start)
        else:
            rev_start = pysvn.Revision(opt_revision_kind.head)

        if end:
            rev_end = end
        else:
            rev_end = 0

        rev_end = pysvn.Revision(opt_revision_kind.number, rev_end)

        opts = {
            'revision_start': rev_start,
            'revision_end': rev_end,
            'limit': limit,
            'discover_changed_paths': paths,
        }

        return self.client.log(dir, **opts)

    def get_log_message(self):
        return self.message

    def get_branch_path(self, name):
        return os.path.join(
            self.repo_url,
            self.root,
            self.branches,
            name
        )

    def get_copy_path(self):
        return os.path.join(
            self.repo_url,
            self.root,
            self.copy_target
        )


class SvynError(Exception):
    pass
