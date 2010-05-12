#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Interfaces relating to users of the wiki."""

from zope.interface import Attribute, Interface


class IUserFactory(Interface):
    """A factory to create `IUser`s."""

    def create(request):
        """Returns an `IUser`."""


class IUser(Interface):
    """Information about the editing user.

    Note: probably implementations
     - test identity
     - bzr identity
     - anonymous identity
     - launchpad identity
     - session identity
    """
    email = Attribute("The user's email adderss.")
    display_name = Attribute(
        "The name that is shown through the user interface.")
    committer_id = Attribute("The user's name and email address.")
