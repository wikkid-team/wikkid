Bazaar Wiki Plugin
==================

Everyone wants a wiki.  Wiki's remember changes.  It makes sense to have
a real DVCS backed wiki.  Hadn't found one for Bazaar, so starting one.


Design Goals
------------

I believe it is better to start with the ideals.  So here goes...

 * Should be able to add the plugin to ~/.bazaar/plugins/wikkid and serve
   any Bazaar branch as a wiki using the command 'bzr wiki <path>'.
 * The rendering of pages needs to be abstracted from the http serving to
   allow the plugin to be used elsewhere as a library (like Launchpad).
 * Use zope interfaces to define clean boundaries between the path traversal,
   rendering, and store access.
 * Have full test coverage.
 * Use a WSGI server for serving over http.
 * Use an existing wiki rendering library so we don't roll our own.
   Current likely contenter is the ReST and/or creoleparser.


Authentication
--------------

This is a bit of an open issue.  For local use we want automagical use
of the identity in the bazaar config file.  However if the wiki is being
served beyond the local machine, there needs to be a place to record
the identity of the editor.
