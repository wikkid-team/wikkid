#! /usr/bin/python
#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The server class for the wiki."""

import logging
import optparse
import sys

from bzrlib.workingtree import WorkingTree

from wikkid.filestore.bzr import FileStore
from wikkid.model.factory import ResourceFactory
from wikkid.twistedserver import TwistedServer
from wikkid.user.bzr import UserFactory


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

    working_tree = WorkingTree.open(options.branch)
    logger.info('Using: %s', working_tree)
    filestore = FileStore(working_tree)
    server = TwistedServer(
        ResourceFactory(filestore),
        UserFactory(working_tree.branch),
        port=options.port)
    server.run()


if __name__ == "__main__":
    main(sys.argv)
