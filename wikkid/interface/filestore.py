#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Interfaces relating to filestores."""

from zope.interface import Attribute, Interface


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
        """Update a text file at the given path with the content.

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

    def list_directory(path):
        """Return a list of IFile objects.

        Each of the IFile objects will be directly in the directory specified
        by the path.

        If the specified path is None, the files in the root directory of the
        branch are returned.

        If the specified path doesn't exist, None is returned.

        If the specified path exists but has no files, an empty list is
        returned.
        """


class FileType(object):
    """Package lazr.enum and use an Enumerated Type."""

    MISSING = 1  # The file at the address does not exist.
    WIKI_PAGE = 2  # The resource is a wiki page.
    DIRECTORY = 3  # The resource is a directory.
    TEXT_FILE = 4  # A text file that isn't a wiki page.
    BINARY_FILE = 5  # A (most likely) binary file.


class IFile(Interface):
    """A file from the file store."""

    path = Attribute(
        "The full path of the page with respect to the root of the "
        "file store.")

    base_name = Attribute("The last part of the path.")

    file_type = Attribute("Soon to be a Choice with a lazr.enum.")

    mimetype = Attribute(
        "The guessed mimetype for the file. Directories don't have a "
        "mimetype.")

    last_modified_in_revision = Attribute(
        "The revision id of the last revision that this file was "
        "modified in.")

    last_modified_by = Attribute("The person who last modified the file.")

    last_modified_date = Attribute(
        'The timestamp of the revision that last modified the file. '
        'This is a naive datetime object in UTC.')

    def get_content():
        """Get the contents of the file.

        :return: None if the file doesn't yet exist, or u'' if the file is
            empty, otherwise the unicode content of the file.
        """
