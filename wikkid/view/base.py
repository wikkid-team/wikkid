#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The base view class."""

import logging

from webob import Response

from wikkid.dispatcher import register_view
from wikkid.view.utils import title_for_filename
from wikkid.interface.resource import IRootResource

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


def canonical_url(context, view=None):
    path = context.preferred_path
    if view is None:
        return path
    else:
        return '{0}/+{1}'.format(path, view)


class BaseView(object):
    """The base view class.

    This is an abstract base class.
    """

    __metaclass__ = BaseViewMetaClass

    def __init__(self, context, request):
        self.context = context
        self.request = request
        if request is not None:
            self.user = request.environ.get('wikkid.user', None)
        self.logger = logging.getLogger('wikkid')

    def _create_breadcrumbs(self):
        crumbs = [Breadcrumb(self.context)]
        parent = getattr(self.context, 'parent', None)
        while parent is not None:
            crumbs.append(Breadcrumb(parent))
            parent = parent.parent
        return reversed(crumbs)

    def initialize(self):
        """Provide post-construction initialization."""

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
            'canonical_url': canonical_url,
            }

    def _render(self, skin):
        """Get the template and render with the args.

        If a template isn't going to be used or provide the conent,
        this is the method to override.
        """
        template = skin.get_template(self.template)
        content = template.render(**self.template_args())
        # Return the encoded content.
        return Response(content.encode('utf-8'))

    def render(self, skin):
        """Render the page.

        Return a tuple of content type and content.
        """
        self.before_render()
        return self._render(skin)


class DirectoryBreadcrumbView(BaseView):
    """A view that uses the directories as breadcrumbs."""

    def _create_breadcrumbs(self):
        crumbs = []
        current = self.context
        suffix = ''
        while not IRootResource.providedBy(current):
            crumbs.append(Breadcrumb(
                    current, suffix, title=current.base_name))
            current = current.parent_dir
            # Add listings to subsequent urls.
            suffix='/+listing'
        # Add in the root dir.
        crumbs.append(Breadcrumb(
                current, url='/+listing', title='wiki root'))
        # And add in the default page.
        crumbs.append(Breadcrumb(current.default_resource))
        return reversed(crumbs)

