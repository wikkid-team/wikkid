#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The wikkid tests and test only code."""

from zope.interface import implementer

from wikkid.interface.user import IUser


class TestUserFactory:
    """Right now, user factories don't do anything."""


@implementer(IUser)
class TestUser:
    """A test user that implements the interface."""

    def __init__(self, email, display_name):
        self.email = email
        self.display_name = display_name
        self.committer_id = f"{email} <{display_name}>"


class TestRequest:
    """A fake request object."""
