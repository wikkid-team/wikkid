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
from wikkid.view.utils import title_for_filename


class BaseViewMetaClass(type):
    """This metaclass registers the view with the view registry."""

    def __new__(cls, classname, bases, classdict):
        """Called when defining a new class."""
        instance = type.__new__(cls, classname, bases, classdict)
        register_view(instance)
        return instance


class Breadcrumb(object):
    """Breadcrumbs exist to give the user quick links up the path chain."""

    def __init__(self, context, suffix='', url=None, title=None):
        if url is not None:
            self.path = url
        else:
            self.path = context.path + suffix
        if title is None:
            self.title = title_for_filename(context.base_name)
        else:
            self.title = title


class BaseView(object):
    """The base view class.

    This is an abstract base class.
    """

    __metaclass__ = BaseViewMetaClass

    def __init__(self, context, request, user):
        self.context = context
        self.request = request
        self.user = user
        self.logger = logging.getLogger('wikkid')

    def _create_breadcrumbs(self):
        crumbs = [Breadcrumb(self.context)]
        parent = getattr(self.context, 'parent', None)
        while parent is not None:
            crumbs.append(Breadcrumb(parent))
            parent = parent.parent
        return reversed(crumbs)

    @property
    def breadcrumbs(self):
        return self._create_breadcrumbs()

    @property
    def title(self):
        return title_for_filename(self.context.base_name)

    def before_render(self):
        """A hook to do things before rendering."""

    def template_args(self):
        """Needs to be implemented in the derived classes.

        :returns: A dict of values.
        """
        return {
            'view': self,
            'user': self.user,
            'context': self.context,
            'request': self.request,
            }

    def _render(self, skin):
        """Get the template and render with the args.

        If a template isn't going to be used or provide the conent,
        this is the method to override.
        """
        template = skin.get_template(self.template)
        content = template.render(**self.template_args())
        self.request.setHeader(
            'Content-Type', "text/html; charset=utf-8")
        # Return the encoded content.
        return content.encode('utf-8')

    def render(self, skin):
        """Render the page.

        Return a tuple of content type and content.
        """
        self.before_render()
        return self._render(skin)
