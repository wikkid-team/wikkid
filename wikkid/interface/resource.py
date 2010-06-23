#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Interfaces for the different resource types."""

from zope.interface import Attribute, Interface


class IDefaultPage(Interface):
    """A marker interface for the default wiki page."""


class IResource(Interface):
    """The base resource interface."""

    path = Attribute('The full path for the resource.')

    preferred_path = Attribute('The preferred path for the resource.')

    write_filename = Attribute(
        'The full path of the file to write to in the filestore. '
        'This is either the filename as it directly corresponds to the '
        'path, or a related wiki page location.')

    root_resource = Attribute(
        'The root resource is the object that represents the root of the wiki.'
        )

    default_resource = Attribute(
        'The default resource is the default wiki page.'
        )


class IUpdatableResource(IResource):
    """Reflects either a file either missing or actual."""

    def put_bytes(bytes, committer, rev_id, commit_msg):
        """Update the content of the resource with the bytes specified.

        :param bytes: A byte string reflecting the new file content.
        :param committer: The committer string that will be used.
        :param rev_id: The base revision id for the text being edited.
            None when adding a new file.
        :param commit_msg: The message to associate with this edit.
        """


class IFileResource(IUpdatableResource):
    """A resource that relates to a file in the filestore."""

    # TODO: think of a better variable name.
    file_resource = Attribute(
        'An IFile representing the file in the filestore.')

    mimetype = Attribute('The mimetype of the file.')

    def get_bytes():
        """Returns the bytes of the binary file."""

    last_modified_in_revision = Attribute(
        'The revision id where the file was last modified.')

    last_modified_by = Attribute(
        'The author of the revision that last modified the file.')

    last_modified_date = Attribute(
        'The timestamp of the revision that last modified the file. '
        'This is a naive datetime object in UTC.')


class IDirectoryResource(IResource):
    """A resource that relates to a file in the filestore."""

    def get_dir_name():
        """Get the full directory name.

        This is the full path for the directory from the root.
        """

    # TODO: think of a better variable name.
    dir_resource = Attribute(
        'An IFile representing the directory in the filestore.')

    def get_listing():
        """Returns a list of objects."""


class IRootResource(IDirectoryResource):
    """A special resource relating to the root object in the wiki."""

    has_home_page = Attribute(
        'True if there is a home wiki page defined.')


class IBinaryFile(IFileResource):
    """A marker interface for binary files."""


class ITextFile(IFileResource):
    """A marker interface for text files."""


class IWikiTextFile(ITextFile):
    """A marker interface for a wiki text file."""


class ISourceTextFile(ITextFile):
    """A marker interface for a non-wiki text file."""


class IMissingResource(IResource):
    """A resource that doesn't exist in the filestore."""
