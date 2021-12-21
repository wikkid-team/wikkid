================
Wikkid Wiki Home
================

Wikkid is a wiki that uses Git or Bazaar as a way to store the content.

Principles of Wikkid
--------------------

* Will run using any Git_ or Bazaar_ branch, not just one it has created
* Provides a Breezy plugin to simplify the serving of a branch
* When run locally Wikkid will use the current users configured identity
* Can be used as a public facing wiki with multiple users
* Can be used as a library in other Python_ applications

.. _Bazaar: https://bazaar.canonical.com
.. _Git: https://git-scm.com/
.. _Python: https://python.org

Quickstart
----------

To run from source, type something like::

    $ python3 setup.py develop  # install dependencies
    $ git init /tmp/wiki
    $ ./bin/wikkid-serve /tmp/wiki
    $ sensible-browser http://localhost:8080/

Or, using docker::

    $ docker run -p 8080:8080 -v /path/to/some/repo:/data \
      ghcr.io/wikkid-team/wikkid
    $ sensible-browser http://localhost:8080/

Now what?
---------

* Join the `developer's mailing list`_
* Read the hacking_ document
* Browse the source_
* Look through the `To Do`_ list and fix something

.. _`developer's mailing list`: https://launchpad.net/~wikkid-dev
.. _hacking: Hacking.txt
.. _source: /+listing
.. _`To Do`: ToDo.txt
