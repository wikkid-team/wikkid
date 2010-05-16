#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The formatter registry is able to return formatters by name."""

import re

from wikkid.formatter.creoleformatter import CreoleFormatter
from wikkid.formatter.pygmentsformatter import PygmentsFormatter
from wikkid.formatter.restformatter import RestructuredTextFormatter


class FormatterRegistry(object):
    """Has a dictionary of formatters based on name."""

    def __init__(self):
        self._formatters = {
            'rest': RestructuredTextFormatter(),
            'creole': CreoleFormatter(),
            'pygments': PygmentsFormatter()
            }

    def __getitem__(self, formatter):
        return self._formatters[formatter]


formatter_registry = FormatterRegistry()


def get_formatter(name):
    """Get a formatter by name."""
    return formatter_registry[name]


FORMAT_MATCHER = re.compile('^#\W+(\w+).*$')


def get_wiki_formatter(content, default_formatter):
    """Choose a wiki formatter based on the first line of content.

    :param content: The content of the file.
    :param default_formatter: The name of the default formatter.

    The first line of the content may specify a formatter using the form:
    # formatter-name

    For example:
    # creole

    The first line must start with a # and the first word must specify
    a formatter name.  If niether of those match, the default_formatter
    is returned.  If the default_formatter doesn't exist, a key error
    is raised.
    """
    end_of_line = content.find('\n')
    match = FORMAT_MATCHER.match(content[:end_of_line])
    if match is not None:
        try:
            formatter = formatter_registry[match.group(1)]
            return content[end_of_line + 1:], formatter
        except KeyError:
            # Fall through to returning the default.
            pass
    return content, formatter_registry[default_formatter]
