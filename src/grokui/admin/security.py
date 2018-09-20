"""Security notifications for `grokui.admin`.

The machinery to do home-calling security notifications.
"""
import grok
import time
import sys

from persistent import Persistent
from grokui.admin.interfaces import ISecurityNotifier
from grokui.admin.utilities import getVersion, TimeoutableHTTPHandler
from grokui.base import Messages, IGrokUIRealm

if sys.version_info >= (3, 3):
    import urllib.request as urllib
    from html import escape
    from urllib.parse import urlparse, urljoin
else:
    import urllib2 as urllib
    from cgi import escape
    from urlparse import urlparse, urljoin


MSG_DISABLED = u'Security notifications are disabled.'


class SecurityNotificationViewlet(grok.Viewlet):
    """Viewlet displaying notifications from a local `SecurityNotifier`.
    """
    grok.order(40)
    grok.context(IGrokUIRealm)
    grok.viewletmanager(Messages)

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
        notifier = self.security_notifier
        if notifier is None:
            return u""
        return u'''<div class="grokui-security message">%s</div>''' % (
            self.security_notifier.getNotification())


class SecurityNotifier(Persistent):
    """A security notifier.

    It can be placed in a site to store notification dates and other
    data persistently.
    """
    grok.implements(ISecurityNotifier)

    VERSION = 1 # for possibly updates/downgrades
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
            return MSG_DISABLED
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
        url = urljoin(self.lookup_url, filename)
        # We create a HTTP handler with a timeout.
        http_handler = TimeoutableHTTPHandler(timeout=self.lookup_timeout)
        opener = urllib.build_opener(http_handler)
        req = urllib.Request(url)
        try:
            message = opener.open(req).read()
            self._message = escape(message.decode())
            self._warningstate = True
        except urllib.HTTPError as e:
            if e.code == 404:
                # No security warning found, good message.
                self._message = u''
                self._warningstate = False
            else:
                raise
        if self._message == MSG_DISABLED:
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
