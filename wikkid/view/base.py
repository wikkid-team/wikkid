#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The base view class."""

import logging

from webob import Response

from wikkid.dispatcher import register_view
from wikkid.view.urls import canonical_url
from wikkid.view.utils import title_for_filename
from wikkid.interface.resource import IDefaultPage, IRootResource


class BaseViewMetaClass(type):
    """This metaclass registers the view with the view registry."""

    def __new__(cls, classname, bases, classdict):
        """Called when defining a new class."""
        instance = type.__new__(cls, classname, bases, classdict)
        register_view(instance)
        return instance


class Breadcrumb(object):
    """Breadcrumbs exist to give the user quick links up the path chain."""

    def __init__(self, context, request, view=None, title=None):
        self.path = canonical_url(context, request, view)
        if title is None:
            self.title = title_for_filename(context.base_name)
        else:
            self.title = title


class BaseView(object, metaclass=BaseViewMetaClass):
    """The base view class.

    This is an abstract base class.
    """

    def __init__(self, context, request, execution_context):
        self.execution_context = execution_context
        self.context = context
        self.request = request
        if request is not None:
            self.user = request.environ.get('wikkid.user', None)
        self.logger = logging.getLogger('wikkid')

    def _create_breadcrumbs(self):
        crumbs = [Breadcrumb(self.context, self.request)]
        current = self.context.parent
        while not IRootResource.providedBy(current):
            crumbs.append(Breadcrumb(current, self.request))
            current = current.parent
        # And add in the default page if the context isn't the default.
        if not IDefaultPage.providedBy(self.context):
            crumbs.append(Breadcrumb(current.default_resource, self.request))
        return reversed(crumbs)

    def initialize(self):
        """Provide post-construction initialization."""

    @property
    def breadcrumbs(self):
        return self._create_breadcrumbs()

    @property
    def title(self):
        return title_for_filename(self.context.base_name)

    @property
    def last_modified_by(self):
        return self.context.last_modified_by

    @property
    def last_modified_date(self):
        last_modified = self.context.last_modified_date
        if last_modified is None:
            return None
        return last_modified.strftime('%Y-%m-%d %H:%M:%S')

    def before_render(self):
        """A hook to do things before rendering."""

    def canonical_url(self, context, view=None):
        return canonical_url(context, self.request, view)

    def template_args(self):
        """Needs to be implemented in the derived classes.

        :returns: A dict of values.
        """
        return {
            'view': self,
            'user': self.user,
            'context': self.context,
            'request': self.request,
            'canonical_url': self.canonical_url,
            }

    def _render(self, skin):
        """Get the template and render with the args.

        If a template isn't going to be used or provide the conent,
        this is the method to override.
        """
        template = skin.get_template(self.template)
        content = template.render(**self.template_args())
        # Return the encoded content.
        return self.make_response(content.encode('utf-8'))

    def make_response(self, body):
        """Construct the response object for this request.

        :param body: The body of the response, as a unicode string.
        :return: A `Response` object.
        """
        return Response(body)

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
        view = None
        while not IRootResource.providedBy(current):
            crumbs.append(Breadcrumb(
                    current, self.request, view, title=current.base_name))
            current = current.parent
            # Add listings to subsequent urls.
            view = 'listing'
        # Add in the root dir.
        crumbs.append(Breadcrumb(current, self.request, 'listing',
                                 title='wiki root'))
        # And add in the default page.
        crumbs.append(Breadcrumb(current.default_resource, self.request))
        return reversed(crumbs)
