#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View classes to control the rendering of the content."""

from wikkid.formatter.pygmentsformatter import PygmentsFormatter
from wikkid.interface.resource import ISourceTextFile
from wikkid.view.base import DirectoryBreadcrumbView


class SourceTextPage(DirectoryBreadcrumbView):
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
