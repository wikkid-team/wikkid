#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The model class for file resources."""

from zope.interface import implementer

from wikkid.model.baseresource import BaseResource
from wikkid.interface.resource import IFileResource, IUpdatableResource
from wikkid.user.bzr import create_bzr_user_from_author_string


@implementer(IUpdatableResource)
class UpdatableResource(BaseResource):
    """Reflects either a file either missing or actual."""

    def put_bytes(self, content: bytes, committer, rev_id, commit_msg):
        """Update the file resource."""
        self.factory.filestore.update_file(
            self.write_filename, content, committer, rev_id, commit_msg)


@implementer(IFileResource)
class FileResource(UpdatableResource):
    """Anything that relates to all files."""

    @property
    def mimetype(self):
        return self.file_resource.mimetype

    @property
    def last_modified_in_revision(self):
        return self.file_resource.last_modified_in_revision

    @property
    def last_modified_date(self):
        return self.file_resource.last_modified_date

    @property
    def last_modified_by(self):
        return create_bzr_user_from_author_string(
            self.file_resource.last_modified_by)

    def get_bytes(self):
        return self.file_resource.get_content()
