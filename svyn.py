

"""svyn.svyn: provides entry point main()."""


__version__ = "0.1.0"

import pysvn
import optparse


def init_parser():
    p = optparse.OptionParser()
    return p


def valid(otps, args):
    pass


def main():
    p = init_parser()
    opts, args = p.parse_args()
    # Validate args.
    if not valid(opts, args):
        p.print_help()
    # Determine command.
    cmd = args[0]
    # Execute command with options and arguments.
    s = Svyn()
    s.execute(cmd, args[1:], opts)


class Svyn():
    pass
