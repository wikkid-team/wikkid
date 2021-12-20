#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The wikkid tests and test only code."""

from zope.interface import implementer

from wikkid.interface.user import IUser


class TestUserFactory(object):
    """Right now, user factories don't do anything."""


@implementer(IUser)
class TestUser(object):
    """A test user that implements the interface."""

    def __init__(self, email, display_name):
        self.email = email
        self.display_name = display_name
        self.committer_id = "{0} <{1}>".format(email, display_name)


class TestRequest(object):
    """A fake request object."""
