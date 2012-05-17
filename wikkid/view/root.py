#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View classes for the wiki root."""

from webob.exc import HTTPSeeOther

from wikkid.interface.resource import IRootResource
from wikkid.view.base import BaseView


class RootPage(BaseView):
    """The default view for the root page redirects to the home page."""

    for_interface = IRootResource
    name = 'view'
    is_default = True

    def _render(self, skin):
        """Redirect to Home (or the default page)."""
        default_resource = self.context.default_resource
        location = self.canonical_url(default_resource)
        raise HTTPSeeOther(location=location)
