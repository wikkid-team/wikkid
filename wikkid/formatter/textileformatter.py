# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A text to html formatter using textile."""


from textile import textile
from zope.interface import implementer

from wikkid.interface.formatter import ITextFormatter


@implementer(ITextFormatter)
class TextileFormatter(object):
    """Format source files as HTML using textile."""

    def format(self, filename, text):
        """Format the text.
        """
        return textile(text)
