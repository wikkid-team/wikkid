#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The base user implementation.

Provides the gravatar support.
"""

import hashlib


class BaseUser(object):

    @property
    def gravatar(self):
        url = "http://www.gravatar.com/avatar/"
        url += hashlib.md5(self.email.lower().encode('utf-8', 'replace')).hexdigest()
        url += "?s=50&d=identicon"
        return url
