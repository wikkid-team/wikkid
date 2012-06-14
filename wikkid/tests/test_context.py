#
# Copyright (C) 2010-2012 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for method and classes in wikkid.context."""

from testtools.matchers import Equals

from wikkid.context import ExecutionContext
from wikkid.tests import TestCase


class TestContext(TestCase):

    def test_empty_script_name(self):
        context = ExecutionContext()
        self.assertThat(context.script_name, Equals(''))

    def test_script_name(self):
        context = ExecutionContext(script_name='/foo')
        self.assertThat(context.script_name, Equals('/foo'))

    def test_script_name_strips_trailing_slash(self):
        context = ExecutionContext(script_name='/foo/')
        self.assertThat(context.script_name, Equals('/foo'))
