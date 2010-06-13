#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A user factory and user class which uses the bzr identity from the
local bazaar config."""

import email
import logging
from zope.interface import implements

from wikkid.interface.user import IUser, IUserFactory
from wikkid.user.baseuser import BaseUser


def create_bzr_user_from_author_string(author):
    name, address = email.Utils.parseaddr(author)
    if name:
        display_name = name
    else:
        display_name = address
    return User(address, display_name, author)


class UserFactory(object):
    """Generate a user from local bazaar config."""

    implements(IUserFactory)

    def __init__(self, branch):
        """Use the user config from the branch."""
        config = branch.get_config()
        self.user = create_bzr_user_from_author_string(config.username())
        logger = logging.getLogger('wikkid')
        logger.info(
            'Using bzr identity: "%s", "%s"',
            self.user.display_name, self.user.email)

    def create(self, request):
        """Create a User."""
        return self.user


class User(BaseUser):
    """A user from the local bazaar config."""

    implements(IUser)

    def __init__(self, email, display_name, committer_id):
        self.email = email
        self.display_name = display_name
        self.committer_id = committer_id

