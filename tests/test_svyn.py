# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import mock
import unittest
from svyn.svyn import Svyn


class TestSvyn(unittest.TestCase):

    def setUp(self):
        pass

    @mock.patch('svyn.svyn.pysvn.Client')
    def test_svyn_branch(self, mock_client):
        config = {
            "repo_root_dir": "svn+ssh://svnroot",
            "branches_dir": "test_branches",
            "copy_target_dir": "test_trunk"
        }
        s = Svyn(config, mock_client)
        mock_opts = mock.MagicMock()
        s.branch("new_branch", mock_opts)
        expected_copy = os.path.join(
            config['repo_root_dir'],
            config['copy_target_dir']
        )
        expected_branch = os.path.join(
            config['repo_root_dir'],
            config['branches_dir'],
            "new_branch"
        )
        mock_client.copy.assert_called_with(expected_copy, expected_branch)
