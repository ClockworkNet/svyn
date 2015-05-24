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
            "copy_source_dir": "test_trunk",
            "releases_dir": "test_tags"
        }
        self.mock_client = mock_client
        self.s = SvynWorker(self.config, mock_client)

        self.releases = ['0.8.2', '0.8.3', '1.0.0', '1.0.1', '1.0.1a',
                         '1.0.1b']

    def test_svyn_branch(self):
        mock_opts = mock.MagicMock()
        self.s.branch("new_branch", mock_opts)
        expected_copy = os.path.join(
            self.config['repo_url'],
            self.config['root_dir'],
            self.config['copy_source_dir']
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

    def test_svyn_release_clean(self):
        target_rev = 1234
        self.mock_client.list = mock.MagicMock()
        self.mock_client.list.return_value = self.releases

        self.s.release(target_rev)

        expected_copy = os.path.join(
            self.config['repo_url'],
            self.config['root_dir'],
            self.config['copy_source_dir']
        )
        expected_release = os.path.join(
            self.config['repo_url'],
            self.config['root_dir'],
            self.config['releases_dir'],
            "1.0.2"
        )

        (copy, release), kwargs = self.mock_client.copy.call_args
        rev = kwargs['src_revision']

        self.assertEqual(rev.number, target_rev)
        self.assertEqual(copy, expected_copy, "Bad copy path: {}".format(copy))
        self.assertEqual(release, expected_release,
                         "Bad release path: {}".format(release))

    def test_svyn_get_next_release(self):
        self.mock_client.list = mock.MagicMock()
        self.mock_client.list.return_value = self.releases

        next = self.s.get_next_release()
        self.assertEqual(next, '1.0.2', 'Bad point release: {}'.format(next))

        next = self.s.get_next_release('minor')
        self.assertEqual(next, '1.1.0', 'Bad minor release: {}'.format(next))

        next = self.s.get_next_release('major')
        self.assertEqual(next, '2.0.0', 'Bad major release: {}'.format(next))

        next = self.s.get_next_release('subtag')
        self.assertEqual(next, '1.0.1c', 'Bad subtag: {}'.format(next))

    def test_svyn_switch(self):
        self.s.switch('path', 'repo')
        self.mock_client.switch.assert_called_with(
            'path',
            'repo'
        )
