#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A text to html formatter using pygments."""

import cgi

from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
from zope.interface import implementer

from wikkid.interface.formatter import ITextFormatter


@implementer(ITextFormatter)
class PygmentsFormatter(object):
    """Format source files as HTML using pygments."""

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
