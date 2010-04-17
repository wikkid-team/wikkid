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

"""Interfaces relating to filestores."""

from zope.interface import Attribute, Interface
from zope.schema import TextLine


class IFileStore(Interface):
    """A file store is how pages are accessed and updated.

    This interface defines methods for getting file contents, checking to see
    if the file exists, updating files, checking differences, and many other
    wiki type thiings.
    """

    def get_file(path):
        """Return an object representing the file at specified path."""

    def update_file(path, content, author, parent_revision,
                    commit_message=None):
        """Update the file at the given path with the content.

        :param path: The path of the file.
        :param content: The content of the file.
        :param author: Who is doing the updating.
        :type author: String
        :param parent_revision: The revision that the user was editing when
           they made the changes.  For a new revision this parameter will be
           None.
        :type parent_revision: String
        :param commit_message: An optional commit message.  If one isn't
           provided, then some sensible default will be used.
        """


class FileType(object):
    """Package lazr.enum and use an Enumerated Type."""
    MISSING = 1 # The file at the address does not exist.
    WIKI_PAGE = 2 # The resource is a wiki page.
    DIRECTORY = 3 # The resource is a directory.
    TEXT_FILE = 4 # A text file that isn't a wiki page.
    BINARY_FILE = 5 # A (most likely) binary file.


class IFile(Interface):
    """A file from the file store."""

    path = TextLine(
        description=(
            u"The full path of the page with respect to the root of the "
            "file store."))

    base_name = TextLine(
        description=(u"The last part of the path."))

    file_id = TextLine(
        description=(
            u"The unique identifier for the file in the filestore."))

    file_type = Attribute("Soon to be a Choice with a lazr.enum.")

    mimetype = TextLine(
        description=(
            u"The guessed mimetype for the file. Directories don't have a "
            "mimetype."))

    last_modified_in_revision = TextLine(
        description=(
            u"The revision id of the last revision that this file was "
            "modified in."))

    last_modified_by = TextLine(
        description=(
            u"The person who last modified the file."))

    def get_content():
        """Get the contents of the file.

        :return: None if the file doesn't yet exist, or u'' if the file is
            empty, otherwise the unicode content of the file.
        """
