import logging
import sys

from breezy.commands import Command
from breezy.option import Option

from breezy.workingtree import WorkingTree

from wikkid.app import WikkidApp
from wikkid.filestore.bzr import FileStore
from wikkid.user.bzr import LocalBazaarUserMiddleware

DEFAULT_PORT = 8080


def setup_logging():
    """Set up a logger sending to stderr."""
    handler = logging.StreamHandler(sys.stderr)
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
        Option(
            'port',
            help='Port to listen, defaults to 8080.',
            type=int,
            short_name='p')
        ]

    def run(self, branch=u'.', port=8080):
        setup_logging()
        logger = logging.getLogger('wikkid')
        logger.setLevel(logging.DEBUG)

        working_tree = WorkingTree.open(branch)
        logger.info('Using: %s', working_tree)
        filestore = FileStore(working_tree)

        app = WikkidApp(filestore)
        app = LocalBazaarUserMiddleware(app, working_tree.branch)
        from wsgiref.simple_server import make_server
        httpd = make_server('localhost', port, app)
        logger.info('Serving on http://localhost:%s', port)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info('Done.')
