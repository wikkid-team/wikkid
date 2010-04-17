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
import logging
from zope.interface import implements

from wikkid.interface.user import IUser, IUserFactory
from wikkid.user.baseuser import BaseUser


class UserFactory(object):
    """Generate a user from local bazaar config."""

    implements(IUserFactory)

    def __init__(self, branch):
        """Use the user config from the branch."""
        config = branch.get_config()
        self.committer_id = config.username()
        name, address = email.Utils.parseaddr(self.committer_id)
        self.email = address
        if name:
            self.display_name = name
        else:
            self.display_name = address
        logger = logging.getLogger('wikkid')
        logger.info(
            'Using bzr identity: "%s", "%s"', self.display_name, self.email)

    def create(self, request):
        """Create a User."""
        return User(self.email, self.display_name, self.committer_id)


class User(BaseUser):
    """A user from the local bazaar config."""

    implements(IUser)

    def __init__(self, email, display_name, committer_id):
        self.email = email
        self.display_name = display_name
        self.committer_id = committer_id

