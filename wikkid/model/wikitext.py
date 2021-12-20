#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The wiki text class.

A text file that contains text that will be formatted into HTML using one of
the formatters.
"""

from zope.interface import directlyProvides, implementer

from wikkid.model.directory import DirectoryMethods
from wikkid.model.textfile import TextFile
from wikkid.interface.resource import IDirectoryResource, IWikiTextFile


@implementer(IWikiTextFile)
class WikiTextFile(TextFile, DirectoryMethods):
    """A text file that represents a wiki page."""

    def __init__(self, server, path, write_filename,
                 file_resource, dir_resource):
        super(WikiTextFile, self).__init__(
            server, path, write_filename, file_resource, dir_resource)
        if dir_resource is not None:
            directlyProvides(self, IDirectoryResource)

    def __repr__(self):
        return "<WikiTextFile '%s'>" % self.path
