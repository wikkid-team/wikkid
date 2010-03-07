#! /usr/bin/python
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

"""The server class for the wiki."""

import logging
import optparse
import sys

from bzrlib.branch import Branch

from wikkid.bzr.filestore import FileStore
from wikkid.server import Server
from wikkid.twistedserver import TwistedServer


def setup_logging():
    """Set up a logger sending to stderr."""
    handler = logging.StreamHandler(strm=sys.stderr)
    fmt = '%(asctime)s %(levelname)-7s %(message)s'
    formatter = logging.Formatter(
        fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.addHandler(handler)


def main(args):
    parser = optparse.OptionParser(
        description="Run a Wikkid Wiki server.")
    parser.add_option('--branch', help='The branch to use as a wiki.')
    parser.add_option('--port', type='int', default=8080,
                      help='The port to listen on.  Defaults to 8080.')
    options, args = parser.parse_args(sys.argv[1:])
    if len(args):
        print "Unexpected positional args:", args
        sys.exit(1)
    setup_logging()
    logger = logging.getLogger('wikkid')
    logger.setLevel(logging.DEBUG)

    branch = Branch.open(options.branch)
    logger.info('Using branch: %s', branch)
    filestore = FileStore(branch)
    # Don't use the user factory yet...
    user_factory = None
    server = TwistedServer(
        Server(filestore, user_factory, logger=logger),
        port=options.port, logger=logger)
    server.run()


if __name__ == "__main__":
    main(sys.argv)
