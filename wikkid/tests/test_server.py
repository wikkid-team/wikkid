#
# Copyright (C) 2010 Wikkid Developers
#
# This file is part of Wikkid.
#
# Wikkid is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wikkid.  If not, see <http://www.gnu.org/licenses/>

"""Tests for the wikkid.server."""

from testtools import TestCase


class TestServer(TestCase):
    """Tests for the Wikkid Server.

    I'm going to write a few notes here.  I want to make sure that the server
    has meaningful names, but also is functional enough.  I have been thinking
    over the last few days that the IFile inteface needs to expose the file-id
    of the underlying file for those cases where the file is moved by one
    person, and edited by another.  I makes sense to use the functionality of
    bzr here to have good editing while moving the file.

    Also since I want this designed in a way that it will integrate well into
    Launchpad, we need to expose partial rendering of the underlying files
    through the interface.  There may well be images or binaries stored as
    part of the branch that need to be served directly (or as directly as
    possible), but also we need to be able to access the rendered page before
    any rendering into a skin.

    I want to provide meaningful directory type listings, but that also means
    doing the on-the-fly conversion of files to 'wiki pages'.  We then want to
    be able to traverse a directory, and product a list of tuples (or objects)
    which define the display name, filename, and mimetype.

    Wiki pages are going to be quite tightly defined.  Must have a wiki name
    (Sentence case joined word), ending in '.txt'.
    """


    def test_something(self):
        pass
