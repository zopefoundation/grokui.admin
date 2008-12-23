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
from grokui.admin.utilities import getVersion, TimeoutableHTTPHandler

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
        event handler triggered on startup.
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
    DEFAULT_URL = 'http://grok.zope.org/releaseinfo/'
    
    lookup_url = DEFAULT_URL
    last_lookup = None   # When did we do the last lookup?
    lookup_timeout = 2   # Number of seconds to wait
    enabled = False      # By default we disable the notfier.

    lookup_frequency = 3600 # Lookup every hour.

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
        version = getVersion('grok')
        filename = 'grok-%s.security.txt' % version
        url = urlparse.urljoin(self.lookup_url, filename)
        # We create a HTTP handler with a timeout.
        http_handler = TimeoutableHTTPHandler(timeout=self.lookup_timeout)
        opener = urllib2.build_opener(http_handler)
        req = urllib2.Request(url)
        try:
            self._message = opener.open(req).read()
            self._warningstate = True
        except (urllib2.HTTPError, OSError), e:
            if (getattr(e, 'code', None) == 404) or (
                getattr(e, 'errno', None) == 2):
                # No security warning found, good message.
                self._message = u''
                self._warningstate = False
        except:
            # An unexpected problem occured...
            pass
        if self._message == self.MSG_DISABLED:
            self._message = u''
        self.last_lookup = time.time()
        return

    def setLookupURL(self, url):
        """Set the url to lookup notifications.
        """
        self.lookup_url = url
        self.last_lookup = None
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
