#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A text to html formatter using reStuctured Text."""

from zope.interface import implements

from wikkid.contrib.creole_1_1.creole import Parser, Rules
from wikkid.contrib.creole_1_1.creole2html import HtmlEmitter

from wikkid.interface.formatter import ITextFormatter


# TODO: automatic registration of formatters with the soon to exist
# FormatFactory (like the ways views are).  Although we may want to auto
# register a lazy loaded formatter.  That way we can have a fall back that
# lets the user (wiki owner) know that there are possible missing
# dependancies.

class CreoleFormatter(object):
    """Format text as HTML using creole wiki format."""

    implements(ITextFormatter)

    def __init__(self):
        self.rules = Rules(wiki_words=True)

    def format(self, filename, text):
        """Format the text."""
        return HtmlEmitter(Parser(text, self.rules).parse()).emit()
