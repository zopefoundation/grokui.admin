grokui.admin changes
********************

1.1 (unreleased)
================

- Nothing changed yet.


1.0 (2023-08-28)
================

- Drop support for Python 2.7, 3.5, 3.6.

- Add support for Python 3.7, 3.8, 3.9, 3.10, 3.11.

- Caution: With this release the maintenance of this package ends.


0.13 (2020-08-20)
=================

- Python3.6+ compatibility.

0.12 (2016-02-16)
=================

- Update to follow API changes in grok.

- Update tests.

0.11 (2012-05-02)
=================

- Make sure to require the latest grok and grokcore.site.

0.10 (2011-07-14)
=================

- Changes not recorded.

0.9 (2011-01-20)
================

- Use the correct IApplication interface definition.

0.8 (2010-10-27)
================

- In testing the security notifications, start a server instead of using
  file://localhost URLs. This saves a lot of urlopen troubles across
  platforms.

- Test setup cleanup.

0.7.2 (2010-10-26)
==================

- Fix tests in Windows.

0.7.1 (2010-10-07)
==================

* Fix a bug in the test setup where zope.session was not configurred.

* Fix https://bugs.launchpad.net/grok/+bug/638763
  We don't hide away Duplication/KeyErrors that are raised during
  application creation any more.

0.7.0 (2010-07-04)
==================

* The application creation view now uses the Grok util function
  `create_application`. Therefore, the `ApplicationInitializedEvent`,
  recently introduced in Grok, is now triggered while an application is
  created and persisted. This is an important event, allowing to hook
  handlers that need local utilities and catalog indexes that are not
  yet present at the ObjectCreatedEvent stage.

0.6.2 (2010-05-19)
==================

* Modified package to comply with Zope Foundation policy.

* Removed duplicated/unused code.
  Fix https://bugs.launchpad.net/grok/+bug/539940

* Reflect changes in Folder API: check also for KeyError, not only for
  DuplicationError when adding new apps.

* Added extra-templatedirs and moved templates into these in order to
  avoid (erraneous) templatedir-registry warnings.

0.6.1 (2010-03-07)
==================

* Added missing tests dependencies. Declarations and includes should
  now be complete.


0.6 (2010-02-28)
================

* Moved the ``Index`` view to ``grokui.base``.

* The design has been slightly changed to get rid of the lazy Grok and
  to match the http://grok.zope.org website design. The design belongs
  now to ``grokui.base``.

* ``grokui.admin`` has been splitted into several packages. It now depends
  on ``grokui.base`` that provides basic components to create and plug UI
  views. ``grokui.admin`` has been altered to reflect the splitting
  changes and now provides a collection of components that will allow
  you to plug your own administration panels and elements.

* Dependencies have been drastically cut down. We are now using the
  ZTK. The only zope.app package remaining is for the tests.

* Reflect the changes in grokcore.view 1.12 where View and CodeView
  become a single View again.


0.5 (2009-09-15)
================

Feature changes
---------------

* The whole introspector stuff was removed in order to reduce number
  of dependencies.

Bug fixes
---------

* Adding apps now emits IObjectCreated events.


0.4.1 (2010-02-14)
==================

Bug fixes
---------

* Backports of fixes from 0.3.3 version (see below).


0.4 (2009-08-21)
================

Feature changes
---------------

* Added a security notifier to inform users when security issues are
  published on http://grok.zope.org. The notifier must be explicitly
  enabled. You can also run your own site/directory to place security
  notifications.

* Added info views to get important information easier with tools like
  ``curl``. Supported infos:

    - Grok version used

    - Current security notification (if any).

Bug fixes
---------

* Adapting this package to use the new version of grokcore.view
  which splits View into CodeView.

* Upgraded the versions to the alpha 4 list to avoid a dependency
  problem with zope.container versions.

* Include the new grok.View permissions for testing.

0.3.3 (2010-02-14)
==================

Bug fixes
---------

* Fixed bug in object browser: objects that 'booleanized' evaluated to
  ``False`` (empty containers for instance) were not displayed.

0.3.2 (2009-04-10)
==================

* Added dependency for zope.app.preference. This is needed by
  zope.app.apidoc but not always fetched.

0.3.1 (2009-04-09)
==================

* Fixed missing dependencies in setup.py.

0.3 (2008-12-13)
================

Feature changes
---------------

* Added capability to pack ZODBs (thanks to Jasper Spaans).

0.2 (2008-12-01)
================

Feature changes
---------------

* Added capability to rename apps.

0.1.2 (2008-09-28)
==================

* Made server controls dependent from availability of
  `IServerControl`. Otherwise the buttons for restarting or stopping
  the server process are not rendered.


0.1.1 (2008-08-05)
==================

* Fixed wrong links in docgrok template.

* Fixed ftesting.zcml that did not work with Grok 0.13.


0.1 (2008-07-10)
================

Feature changes
---------------

Initial implementation by factoring out ``grok.admin`` from ``grok``.
