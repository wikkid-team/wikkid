#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View classes to control the rendering of the content."""

from twisted.web.util import redirectTo

from wikkid.formatter.pygmentsformatter import PygmentsFormatter
from wikkid.interface.resource import (
    IRootResource,
    ISourceTextFile,
    )
from wikkid.view.base import BaseView, DirectoryBreadcrumbView


class RootPage(BaseView):
    """The default view for the root page redirects to the home page."""

    for_interface = IRootResource
    name = 'view'
    is_default = True

    def _render(self, skin):
        """Redirect to Home (or the default page)."""
        preferred = self.context.preferred_path
        return redirectTo(preferred, self.request)


class OtherTextPage(DirectoryBreadcrumbView):
    """Any other non-binary file is considered other text.

    Will be rendered using pygments.
    """

    for_interface = ISourceTextFile
    name = 'view'
    is_default = True
    template = 'view_page'

    @property
    def content(self):
        formatter = PygmentsFormatter()
        return formatter.format(
            self.context.base_name, self.context.get_bytes())
