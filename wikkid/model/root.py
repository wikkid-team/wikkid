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

"""The root resource class.

The root resource represents the object at the root of the wiki path.

Currently this just refers to '/', but it is expected that at some stage in
the not too distant future the server will support a wiki root where it is not
the root path.
"""

from zope.interface import implements

from wikkid.model.baseresource import BaseResource
from wikkid.interface.resource import IRootResource


class RootResource(BaseResource):
    """The root of the wiki.

    Some special wiki views hang off the root resource and not others.  A root
    resource is also a directory resource where the directory is the root of
    the filesystem.
    """

    implements(IRootResource)
