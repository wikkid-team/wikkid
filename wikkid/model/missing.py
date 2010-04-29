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

"""The missing resource class.

A missing resource is a file that has been asked for that doesn't exist.

A model object exists for a missing resource as in a wiki you can have views
on things that aren't there, like a page asking if you want to make a wiki
page there.
"""

from zope.interface import implements

from wikkid.model.baseresource import BaseResource
from wikkid.interface.resource import IMissingResource


class MissingResource(BaseResource):
    """Information about a resource."""

    implements(IMissingResource)

    # NOTE: perhaps it'll make more sense to put the actual saving or
    # modifying of text content into a base class that both this class and the
    # text file classes can inherit from.

    def __repr__(self):
        return "<MissingResource '%s'>" % self.path
