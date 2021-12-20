#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The binary resource class.

A binary resource is a file that isn't text.  This is primarily guessed using
the mimetype library.
"""

from zope.interface import implementer

from wikkid.model.file import FileResource
from wikkid.interface.resource import IBinaryFile


@implementer(IBinaryFile)
class BinaryResource(FileResource):
    """A binary resource is a non-text file."""

    def __repr__(self):
        return "<BinaryResource '%s'>" % self.path
