#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The model class for file resources."""

from zope.interface import implements

from wikkid.model.baseresource import BaseResource
from wikkid.interface.resource import IFileResource, IUpdatableResource


class UpdatableResource(BaseResource):
    """Reflects either a file either missing or actual."""

    implements(IUpdatableResource)

    def put_bytes(self, bytes, committer, rev_id, commit_msg):
        """Update the file resource."""
        self.server.filestore.update_file(
            self.write_filename, bytes, committer, rev_id, commit_msg)


class FileResource(UpdatableResource):
    """Anything that relates to all files."""

    implements(IFileResource)

    @property
    def mimetype(self):
        return self.file_resource.mimetype

    @property
    def last_modified_in_revision(self):
        return self.file_resource.last_modified_in_revision

    def get_bytes(self):
        return self.file_resource.get_content()
