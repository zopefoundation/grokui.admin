**Caution!**

This package is no longer maintained, its repository has been archived. If you want to work on it please open a ticket in https://github.com/zopefoundation/meta/issues requesting its unarchival.


grokui.admin: A basic grok admin UI
***********************************

The replacement for the former ``grok.admin`` package.

The internal name of the admin UI is:
Grok Application Interface Application or, for short GAIA.

GAIA is itself a Grok application and a subproject to the core Grok
development. Its main goal is making developing of Zope 3 and Grok
applications a faster and smarter job with more fun for everybody.


Login - what is my username/password?
=====================================

Before you can use the admin UI, you first must log in.

The username and password of the manager principal (kind of super
user) can be found in the file ``buildout.cfg`` in the root of your
subversion checkout.

In case you do not know, what 'subversion checkout' means, look for a
file ``site.zcml`` in your installation.

Users of ``grokproject``, might find this file in
``<installdir>/parts/app/site.zcml``.


Using the admin-UI
==================

After login you can visit some of the main management topics, as
described below:

On top of the admin-UI you can always find three links to the main
management activities currently possible with GAIA:


Applications
------------

* List of all instanciated applications

* You can add new instances of Grok applications

* You can rename instances of Grok applications

* You can delete your installed applications.

.. note:: starting with version 0.5 there is no introspector/class
   browser included in `grokui.admin` anymore. Eventually this will be
   made available in another package by someone else.


Server
------

* Set security notifications. Those are by default disabled, because
  they mean home-calling functionality you may do not want. You can
  enable/disable those notifications or set a URL to retrieve
  information about security related problems.

* Start/Restart the server. Caution! This does not work, if the server
  was started in 'foreground mode' (with 'zopectl fg').

* Pack the ZODB. This removes old data from the database, freeing up
  disk space. In a production environment, you might want to pack the
  ZODB automatically from `cron`. This can be done using a command
  like the following::

    curl -q -s -u admin:admin "http://localhost:8080/++grokui++/@@server?pack=1&days=1"

  which will remove old data older than one day. If you leave out the
  `days` parameter, all old data will be removed.

* Get basic information about the running Zope system.

* Enter a message to be displayed on top. You can, for example, leave
  a message here for your co-admins. To delete the message, just enter
  the empty string in the appropriate input box.



Maintaining grok installations with the admin UI
================================================

There are some special info views available especially for the use of
system administrators that want to automate Grok administration in
some aspects. They provide minimal information about certain topics.

Currently the following infos are available this way:

* The grok version working in background::

   curl -q -s -u admin:admin "http://localhost:8080/++grokui++/@@admin/@@version"

* The security notification (if any)::

   curl -q -s -u admin:admin "http://localhost:8080/++grokui++/@@admin/@@secnote"

Beside this you can pack the ZODB databases as described above.
