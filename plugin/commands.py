import logging
import sys

from bzrlib.commands import Command, register_command
from bzrlib.option import Option

from bzrlib.workingtree import WorkingTree

from wikkid.filestore.bzr import FileStore
from wikkid.model.factory import ResourceFactory
from wikkid.twistedserver import TwistedServer
from wikkid.user.bzr import UserFactory

DEFAULT_PORT = 8080

def setup_logging():
    """Set up a logger sending to stderr."""
    handler = logging.StreamHandler(strm=sys.stderr)
    fmt = '%(asctime)s %(levelname)-7s %(message)s'
    formatter = logging.Formatter(
        fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.addHandler(handler)

class cmd_wikkid(Command):
    """Serve branch as a wiki using wikkid."""
    aliases = ['wiki']
    takes_args = ['branch?']
    takes_options = [
        Option('port',
            help = 'Port to listen, defaults to 8080.',
            type = int,
            short_name = 'p')
        ]

    def run(self, branch=u'.', port=8080):
        setup_logging()
        logger = logging.getLogger('wikkid')
        logger.setLevel(logging.DEBUG)

        working_tree = WorkingTree.open(branch)
        logger.info('Using: %s', working_tree)
        filestore = FileStore(working_tree)
        server = TwistedServer(
            ResourceFactory(filestore),
            UserFactory(working_tree.branch),
            port=port)
        server.run()
