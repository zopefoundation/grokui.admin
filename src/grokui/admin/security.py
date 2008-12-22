##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Security notifications for `grokui.admin`.

The machinery to do home-calling security notifications.
"""
import grok
import time
import urllib2
import urlparse
from zope.app.appsetup.interfaces import IDatabaseOpenedWithRootEvent
from zope.app.folder.interfaces import IRootFolder
from zope.component import adapter, provideHandler
from persistent import Persistent
from grokui.admin.interfaces import ISecurityNotifier
from grokui.admin.utilities import getGrokVersion

class SecurityScreen(grok.ViewletManager):
    """A viewlet manager that keeps security related notifications.
    """
    grok.name('grokadmin_security')
    grok.context(IRootFolder)

class SecurityNotificationViewlet(grok.Viewlet):
    """Viewlet displaying notifications from a local `SecurityNotifier`.
    """
    grok.context(IRootFolder)

    @property
    def security_notifier(self):
        """Get a local security notifier.

        The security notifier is installed as a local utility by an
        event handler in the security module.
        """
        site = grok.getSite()
        site_manager = site.getSiteManager()
        return site_manager.queryUtility(ISecurityNotifier, default=None)

    def render(self):
        return self.security_notifier.getNotification()

class SecurityNotifier(Persistent):
    """A security notifier.

    It can be placed in a site to store notification dates and other
    data persistently.
    """

    grok.implements(ISecurityNotifier)

    VERSION = 1 # for possibly updates/downgrades
    MSG_DISABLED = u'Security notifications are disabled.'
    
    lookup_url = 'http://grok.zope.org/releaseinfo/'
    last_lookup = None   # When did we do the last lookup?
    lookup_timeout = 2   # Number of seconds to wait
    last_display = None  # When did we display the last time?
    enabled = False      # By default we disable the notfier.

    lookup_frequency = 3600 * 3 # Lookup every three hours.
    display_frequency = 3600 * 3 # Display warnings every three hours.

    _message = u''
    _warningstate = False
    
    def enable(self):
        """Enable security notifications.
        """
        self.enabled = True
        return

    def disable(self):
        """Disable security notifications.
        """
        self.enabled = False
        return

    def getNotification(self):
        """Get the current security notification.
        """
        if self.enabled is False:
            return self.MSG_DISABLED
        self.updateMessage()
        return self._message

    def isWarning(self):
        self.updateMessage()
        return self._warningstate
    
    def updateMessage(self):
        """Update the security message.
        """
        if self.enabled is False:
            return
        if self.last_lookup is not None:
            if time.time() - self.lookup_frequency < self.last_lookup:
                return
        self.fetchMessage()
        return
    
    def fetchMessage(self):
        """Possibly fetch security notfications from grok.zope.org.
        """
        if self.enabled is False:
            # Safety belt.
            return
        version = getGrokVersion()
        filename = 'grok-%s.security.txt' % version
        url = urlparse.urljoin(self.lookup_url, filename)
        try:
            self._message = urllib2.urlopen(url).read()
        except:
            # Currently we tolerate any error, while only certain
            # ones, like HTTPError 404 or OSError 'File not found'
            # should be accepted.
            #
            # In case of an error we assume, that there is no security
            # notification available.
            self._message = u''
        self.last_lookup = time.time()
        return

    def display(self):
        """Display the message.

        In fact we only keep track of timestamps of display actions.
        """
        self.last_display = time.time()
        return

def setupSecurityNotification(site):
    """Setup a SecurityNotifier as persistent utility.

    The utility is installed as a local and persistent utility. It is
    local to `site` and installed under the name
    ``grokadmin_security`` in the site manager of `site`.

    It can be retrieved with a call like::

      site.getSiteManager().getUtiliy(ISecurityNotifier)

    See also ``security.py`` in ``tests``.
    """
    site_manager = site.getSiteManager()
    if 'grokadmin_security' not in site_manager:
        site_manager['grokadmin_security'] = SecurityNotifier()
    utility = site_manager['grokadmin_security']
    site_manager.registerUtility(utility, ISecurityNotifier, name=u'')
    return
    
@adapter(IDatabaseOpenedWithRootEvent)
def securitySetupHandler(event):
    """Call security notification setup as soon as DB is ready.
    """
    from zope.app.appsetup.bootstrap import getInformationFromEvent
    
    db, connection, root, root_folder = getInformationFromEvent(event)
    setupSecurityNotification(root_folder)
    
# ...then install the event handler:
provideHandler(securitySetupHandler)
