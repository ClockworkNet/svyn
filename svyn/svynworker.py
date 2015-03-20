
import pwd
import os

# Third-party
import pysvn


class SvynWorker(object):
    """Mediates pysvn calls in a nice api. I hope."""

    def __init__(self, cnf, client=None):
        if client is None:
            client = pysvn.Client()
        self.client = client
        self.repo = cnf['repo_url']
        self.root = cnf['root_dir']
        self.copy_source = cnf['copy_source_dir']
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

    def list(self, search=None, mine=False):
        """List all branches."""

        res = self.client.list(
            self.get_branch_path(''),
            recurse=False,
        )

        branches = []
        for (info, _) in res:
            b = info.path.split(os.sep)[-1]

            if search and not search in b:
                continue

            if mine and not self.get_author() in info.last_author:
                continue

            branches.append(b)

        return branches

    def overlap(self, rev1, rev2):
        """Determines if any files have changed in both revisions."""
        pass

    def accumulate_changed_paths(self, rev1, rev2):
        logs = self.fetch_logs(
            self.get_copy_path(),  # Assuming want trunk changes - shady
            start=rev2,
            end=rev1,
        )
        changed_paths = set()
        for l in logs:
            changed_paths.update(p.path for p in l.changed_paths)

        return changed_paths

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
            rev_start = pysvn.Revision(
                pysvn.opt_revision_kind.number,
                start
            )
        else:
            rev_start = pysvn.Revision(pysvn.opt_revision_kind.head)

        if end:
            rev_end = end
        else:
            rev_end = 0

        rev_end = pysvn.Revision(pysvn.opt_revision_kind.number, rev_end)

        opts = {
            'revision_start': rev_start,
            'revision_end': rev_end,
            'limit': limit,
            'discover_changed_paths': paths,
        }

        return self.client.log(dir, **opts)

    def get_branch_path(self, name):
        return os.path.join(
            self.repo,
            self.root,
            self.branches,
            name
        )

    def get_copy_path(self):
        return os.path.join(
            self.repo,
            self.root,
            self.copy_source
        )

    def get_author(self):
        return pwd.getpwuid(os.getuid())[0]


class SvynError(Exception):
    pass
