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

"""A text to html formatter using reStuctured Text."""

from zope.interface import implements

from wikkid.interface.formatter import ITextFormatter


# TODO: automatic registration of formatters with the soon to exist
# FormatFactory (like the ways views are).  Although we may want to auto
# register a lazy loaded formatter.  That way we can have a fall back that
# lets the user (wiki owner) know that there are possible missing
# dependancies.

class CreoleFormatter(object):
    """Format text as HTML using creole wiki format."""

    implements(ITextFormatter)

    def format(self, filename, text):
        """Format the text."""
