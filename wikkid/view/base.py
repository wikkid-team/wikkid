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
import re

from wikkid.dispatcher import register_view


WIKI_PAGE = re.compile('^([A-Z]+[a-z]*)+$')
WIKI_PAGE_ELEMENTS = re.compile('([A-Z][a-z]+)')


def expand_wiki_name(name):
    """A wiki name like 'FrontPage' is expanded to 'Front Page'.

    Names that don't match wiki names are unaltered.
    """
    if WIKI_PAGE.match(name):
        name_parts = [
            part for part in WIKI_PAGE_ELEMENTS.split(name) if part]
        return ' '.join(name_parts)
    else:
        return name


def title_for_filename(filename):
    """Generate a title based on the basename of the file object."""
    if filename.endswith('.txt'):
        return expand_wiki_name(filename[:-4])
    else:
        return expand_wiki_name(filename)


class BaseViewMetaClass(type):
    """This metaclass registers the view with the view registry."""

    def __new__(cls, classname, bases, classdict):
        """Called when defining a new class."""
        instance = type.__new__(cls, classname, bases, classdict)
        register_view(instance)
        return instance


class Breadcrumb(object):
    """Breadcrumbs exist to give the user quick links up the path chain."""

    def __init__(self, context):
        self.path = context.path
        self.title = title_for_filename(context.base_name)


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
        parents = []
        parent = getattr(context, 'parent', None)
        while parent is not None:
            parents.append(Breadcrumb(parent))
            parent = parent.parent
        self.parents = reversed(parents)

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

    def render(self, skin):
        """Render the page.

        Return a tuple of content type and content.
        """
        self.before_render()
        template = skin.get_template(self.template)
        rendered = template.render(**self.template_args())
        return ('text/html', rendered)
