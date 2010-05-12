#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Interface for the text formatters."""


from zope.interface import Interface


class ITextFormatter(Interface):
    """A text formatter takes plain text and makes HTML of some form."""

    def format(filename, text):
        """Takes text, and returns HTML."""
