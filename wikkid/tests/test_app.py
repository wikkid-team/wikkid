#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for method and classes in wikkid.app."""


from wikkid.app import WikkidApp
from wikkid.filestore.volatile import FileStore
from wikkid.tests import TestCase


class TestApp(TestCase):

    def test_traverse_above_static_not_possible(self):
        """
        Traversal above the static folder, by forging a malicious request for
        example, is not possible.
        """
        environ = {
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/static/../page.html",
            }

        def start_response(status, headers):
            self.assertEqual("404 Not Found", status)

        filestore = FileStore()
        app = WikkidApp(filestore)
        app(environ, start_response)
