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

"""The wiki text class.

A text file that contains text that will be formatted into HTML using one of
the formatters.
"""

from zope.interface import implements

from wikkid.model.textfile import TextFile
from wikkid.interface.resource import IWikiTextFile


class WikiTextFile(TextFile):
    """A text file that represents a wiki page."""

    implements(IWikiTextFile)

    def __repr__(self):
        return "<WikiTextFile '%s'>" % self.path
