#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A user factory and user class which uses the git identity from the
local Git config."""

import email
import logging

from webob import Request
from zope.interface import implementer

from wikkid.interface.user import IUser, IUserFactory
from wikkid.user.baseuser import BaseUser


def create_git_user_from_author_string(author):
    name, address = email.Utils.parseaddr(author)
    if name:
        display_name = name
    else:
        display_name = address
    return User(address, display_name, author)


class LocalGitUserMiddleware(object):
    """A middleware to inject a user into the environment."""

    def __init__(self, app, repo):
        self.app = app
        config = repo.get_config_stack()
        email = config.get(("user", ), "email")
        name = config.get(("user", ), "name")
        self.user = User(email, name, "%s <%s>" % (name, email))

    def __call__(self, environ, start_response):
        environ['wikkid.user'] = self.user
        req = Request(environ)
        resp = req.get_response(self.app)
        return resp(environ, start_response)


@implementer(IUserFactory)
class UserFactory(object):
    """Generate a user from local bazaar config."""

    def __init__(self, branch):
        """Use the user config from the branch."""
        config = branch.get_config()
        self.user = create_git_user_from_author_string(config.username())
        logger = logging.getLogger('wikkid')
        logger.info(
            'Using git identity: "%s", "%s"',
            self.user.display_name, self.user.email)

    def create(self, request):
        """Create a User."""
        return self.user


@implementer(IUser)
class User(BaseUser):
    """A user from the local bazaar config."""

    def __init__(self, email, display_name, committer_id):
        self.email = email
        self.display_name = display_name
        self.committer_id = committer_id
