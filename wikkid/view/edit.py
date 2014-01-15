#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""View base class for editing text pages."""

from wikkid.view.base import BaseView
from wikkid.view.utils import expand_wiki_name


class BaseEditView(BaseView):
    """Base class for editing text."""

    name = 'edit'
    template = 'edit_page'

    @property
    def title(self):
        return 'Editing "%s"' % expand_wiki_name(self.context.base_name)

    @property
    def save_url(self):
        """The link for the cancel button."""
        return self.canonical_url(self.context, 'save')

    @property
    def cancel_url(self):
        """The link for the cancel button."""
        return self.canonical_url(self.context)
