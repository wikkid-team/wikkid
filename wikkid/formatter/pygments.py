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

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from zope.interface import implements

from wikkid.interface.formatter import ITextFormatter


class PygmentsFormatter(object):
    """Format source files as HTML using pygments."""

    implements(ITextFormatter)

    def format(self, filename, text):
        """Format the text.

        I'm almost 100% positive that this method needs more args.
        """
        parts = publish_parts(text, writer_name='html')
        return parts['html_title'] + parts['body']
