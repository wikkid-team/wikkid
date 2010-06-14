#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Views associated with binary files."""

from webob import Response

from wikkid.interface.resource import IBinaryFile
from wikkid.view.base import BaseView


class BinaryFile(BaseView):
    """Renders a binary file with its mimetype."""

    for_interface = IBinaryFile
    name = 'view'
    is_default = True

    def _render(self, skin):
        return Response(
            body=self.context.get_bytes(),
            content_type=self.context.mimetype)
