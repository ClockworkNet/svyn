

"""svyn.svyn: provides entry point main()."""


__version__ = "0.1.0"

import ConfigParser
import optparse
import os
import pysvn


def init_optparser():
    p = optparse.OptionParser()
    p.add_option("-s", "--switch",
                 action="store_true", dest="switch", default=False)
    p.add_option("-m", "--message",
                 action="store", type="string", dest="message")
    return p


def init_config():
    """Expects a .svynrc in home folder."""
    cp = ConfigParser.SafeConfigParser()
    try:
        with open(cp.read(os.path.expanduser("~/.svynrc"))) as config:
            cp.readfp(config)
    except IOError:
        raise IOError("Config file expected at ~/.svynrc not found.")
    return cp


def main():
    c = init_config()
    p = init_optparser()
    opts, args = p.parse_args()
    # Determine command.
    cmd = args[0]
    s = Svyn(dict(c.items("svn")))
    # Validate args.
    valid = s.validate_cmd(cmd, args[1:], opts)
    if not valid:
        p.print_help()
    # Execute command with options and arguments.
    getattr(s, cmd)(args[1:], opts)


class Svyn():
    """Mediates pysvn calls in a nice api. I hope."""

    def __init__(self, cnf, client=None):
        if client is None:
            client = pysvn.Client()
        self.client = client
        self.root = cnf['repo_root']
        self.copy_target = cnf['copy_target']
        self.branches = cnf['branches']

        self.client.callback_get_log_message = self.get_log_message

    def branch(self, name, opts):
        """Copy an origin branch to a target specified by name."""
        message = "Branched: " + name
        if opts.message:
            message += "\n" + opts.message
        self.message = message

        branch_path = self.get_branch_path(name)
        copy_path = self.get_copy_path()

        print "branch path: " + branch_path
        print "copy path: " + copy_path

        self.client.copy(copy_path, branch_path)

    def get_log_message(self):
        return self.message

    def get_branch_path(self, name):
        return "%s/%s/%s" % (self.root, self.branches, name)

    def get_copy_path(self):
        return "%s/%s" % (self.root, self.copy_target)

    def validate_command(self, cmd, args, opts):
        return True
