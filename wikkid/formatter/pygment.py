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

"""A text to html formatter using pygments."""

import cgi

from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
from zope.interface import implements

from wikkid.interface.formatter import ITextFormatter


class PygmentsFormatter(object):
    """Format source files as HTML using pygments."""

    implements(ITextFormatter)

    def format(self, filename, text):
        """Format the text.

        We can at a later time try to guess the lexer based on the file
        content.
        """
        try:
            lexer = guess_lexer_for_filename(filename, text)
            return highlight(text, lexer, HtmlFormatter())
        except ClassNotFound:
            return "<pre>{0}</pre>".format(cgi.escape(text))
