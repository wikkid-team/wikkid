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

"""A user factory and user class which uses the bzr identity from the
local bazaar config."""

import email
from zope.interface import implements

from wikkid.interfaces import IUser, IUserFactory


class UserFactory(object):
    """Generate a user from local bazaar config."""

    implements(IUserFactory)

    def __init__(self, branch):
        """Use the user config from the branch."""
        config = branch.get_config()
        name, address = email.Utils.parseaddr(config.username())
        self.email = address
        if name:
            self.display_name = name
        else:
            self.display_name = address

    def create(self, request):
        """Create a User."""
        return User(self.email, self.display_name)


class User(object):
    """A user from the local bazaar config."""

    implements(IUser)

    def __init__(self, email, display_name):
        self.email = email
        self.display_name = display_name

