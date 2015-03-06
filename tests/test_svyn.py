# -*- coding: utf-8 -*-

import sys
import os
import mock
import unittest

sys.path.insert(0, os.path.abspath('..'))
from svyn.svynworker import SvynWorker


class TestSvyn(unittest.TestCase):

    @mock.patch('svyn.svynworker.pysvn.Client')
    def setUp(self, mock_client):
        self.config = {
            "repo_url": "svn+ssh://svnroot",
            "root_dir": "test_code",
            "branches_dir": "test_branches",
            "copy_target_dir": "test_trunk"
        }
        self.mock_client = mock_client
        self.s = SvynWorker(self.config, mock_client)

    def test_svyn_branch(self):
        mock_opts = mock.MagicMock()
        self.s.branch("new_branch", mock_opts)
        expected_copy = os.path.join(
            self.config['repo_url'],
            self.config['root_dir'],
            self.config['copy_target_dir']
        )
        expected_branch = os.path.join(
            self.config['repo_url'],
            self.config['root_dir'],
            self.config['branches_dir'],
            "new_branch"
        )

        self.mock_client.copy.assert_called_with(
            expected_copy,
            expected_branch
        )

    def test_svyn_find(self):
        pass

    def test_svyn_switch(self):
        self.s.switch('path', 'repo')
        self.mock_client.switch.assert_called_with(
            'path',
            'repo'
        )
