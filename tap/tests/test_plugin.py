# Copyright (c) 2015, Matt Layman

import unittest

try:
    from unittest import mock
except ImportError:
    import mock
# There is some weird conflict with `TestLoader.discover` if `nose.case.Test`
# is imported directly. Importing `nose.case` works.
from nose import case

from tap.plugin import TAP


class FakeOptions(object):

    def __init__(self):
        self.tap_outdir = None
        self.tap_format = ''


class FakeTestCase(object):

    def __call__(self):
        pass


class TestPlugin(unittest.TestCase):

    @classmethod
    def _make_one(cls, options=None):
        plugin = TAP()
        plugin.enabled = True
        if options is None:
            options = FakeOptions()
        plugin.configure(options, None)
        return plugin

    def test_adds_error(self):
        plugin = self._make_one()
        plugin.addError(case.Test(FakeTestCase()), (None, None, None))
        line = plugin.tracker._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'not ok')

    def test_adds_skip(self):
        # Since Python versions earlier than 2.7 don't support skipping tests,
        # this test has to hack around that limitation.
        try:
            plugin = self._make_one()
            plugin.addError(case.Test(
                FakeTestCase()), (unittest.SkipTest, 'a reason', None))
            line = plugin.tracker._test_cases['FakeTestCase'][0]
            self.assertEqual(line.directive, '# SKIP a reason')
        except AttributeError:
            self.assertTrue(
                True, 'Pass because this Python does not support SkipTest.')

    @mock.patch('tap.plugin.sys')
    def test_bad_format_string(self, fake_sys):
        """A bad format string exits the runner."""
        options = FakeOptions()
        options.tap_format = "Not gonna work {sort_desc}"
        plugin = self._make_one(options)
        test = mock.Mock()

        plugin._description(test)

        self.assertTrue(fake_sys.exit.called)
