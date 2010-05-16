#
# Copyright (C) 2010 Wikkid Developers
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The formatter registry is able to return formatters by name."""

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
    
    return formatter_registry[default_formatter]
