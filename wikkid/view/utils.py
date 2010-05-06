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

"""Utility methods for wikkid views."""

import re


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
