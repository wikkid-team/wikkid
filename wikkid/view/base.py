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

"""The base view class."""

import logging

from wikkid.dispatcher import register_view


class BaseViewMetaClass(type):
    """This metaclass registers the view with the view registry."""

    def __new__(cls, classname, bases, classdict):
        """Called when defining a new class."""
        instance = type.__new__(cls, classname, bases, classdict)
        register_view(instance)
        return instance


class BaseView(object):
    """The base view class.

    This is an abstract base class.
    """

    __metaclass__ = BaseViewMetaClass

    def __init__(self, skin, resource, path, user):
        self.skin = skin
        self.resource = resource
        self.request_path = path
        self.user = user
        self.logger = logging.getLogger('wikkid')

    def template_args(self):
        """Needs to be implemented in the derived classes.

        :returns: A dict of values.
        """
        return {
            'view': self,
            'user': self.user,
            }

    def render(self):
        """Render the page.

        Return a tuple of content type and content.
        """
        template = self.skin.get_template(self.template)
        rendered = template.render(**self.template_args())
        return ('text/html', rendered)
