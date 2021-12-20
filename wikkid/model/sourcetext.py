#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The source text class.

A source text file is a text file that isn't a wiki file.
"""

from zope.interface import implementer

from wikkid.model.textfile import TextFile
from wikkid.interface.resource import ISourceTextFile


@implementer(ISourceTextFile)
class SourceTextFile(TextFile):
    """A text file that isn't a wiki page."""
