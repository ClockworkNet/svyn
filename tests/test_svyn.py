# -*- coding: utf-8 -*-

import sys
import os
import mock
import unittest
import svyn.svyn


class TestSvyn(unittest.TestCase):

    def setUp(self):
        pass

    @mock.patch('svyn.svyn.pysvn.Client')
    def test_svyn_branch(self, mock_client):
        config = {"repo_root": "svn+ssh://svnroot",
                  "branches": "test_branches",
                  "copy_target": "test_trunk"}
        s = svyn.svyn.Svyn(config, mock_client)
        mock_opts = mock.MagicMock()
        s.branch("new_branch", mock_opts)
        expected_copy = config['repo_root'] + '/' + config['copy_target']
        expected_branch = config['repo_root'] + '/' + config['branches'] + "/new_branch"
        mock_client.copy.assert_called_with(expected_copy, expected_branch)
