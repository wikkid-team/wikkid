#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The missing resource class.

A missing resource is a file that has been asked for that doesn't exist.

A model object exists for a missing resource as in a wiki you can have views
on things that aren't there, like a page asking if you want to make a wiki
page there.
"""

from zope.interface import implementer

from wikkid.model.file import UpdatableResource
from wikkid.interface.resource import IMissingResource


@implementer(IMissingResource)
class MissingResource(UpdatableResource):
    """Information about a resource."""

    def __repr__(self):
        return "<MissingResource '%s'>" % self.path
