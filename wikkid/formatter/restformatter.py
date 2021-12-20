#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A text to html formatter using reStuctured Text."""

from docutils.core import publish_parts
from zope.interface import implementer

from wikkid.interface.formatter import ITextFormatter


@implementer(ITextFormatter)
class RestructuredTextFormatter(object):
    """Format text as HTML using restructured text."""

    def format(self, filename, text):
        """Format the text.

        I'm almost 100% positive that this method needs more args.
        """
        parts = publish_parts(text, writer_name='html')
        return parts['html_title'] + parts['body']
