# -*- coding: utf-8 -*-

import grok
import z3c.flashmessage.interfaces

from grokui.base.layout import GrokUIView
from grokui.admin.interfaces import ISecurityNotifier
from grokui.admin.utilities import getVersion
from grokui.admin.security import SecurityNotifier

from ZODB.interfaces import IDatabase
from ZODB.FileStorage.FileStorage import FileStorageError

from zope.size import byteDisplay
from zope.site.interfaces import IRootFolder
from zope.applicationcontrol.interfaces import IServerControl, IRuntimeInfo
from zope.applicationcontrol.applicationcontrol import applicationController
from zope.component import getUtility, queryUtility, getUtilitiesFor
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('grokui')


class Server(GrokUIView):
    """Zope3 management screen.
    """
    grok.title('Server Control')
    grok.require('grok.ManageApplications')

    _fields = (
        "ZopeVersion",
        "PythonVersion",
        "PythonPath",
        "SystemPlatform",
        "PreferredEncoding",
        "FileSystemEncoding",
        "CommandLine",
        "ProcessId",
        "DeveloperMode",
        )

    _unavailable = _("Unavailable")

    @property
    def grok_version(self):
        return getVersion('grok')

    @property
    def grokuiadmin_version(self):
        return getVersion('grokui.admin')

    def root_url(self, name=None):
        obj = self.context
        while obj is not None:
            if IRootFolder.providedBy(obj):
                return self.url(obj, name)
            obj = obj.__parent__
        raise ValueError("No application nor root element found.")

    @property
    def security_notifier_url(self):
        """Get the URL to look up for security warnings.
        """
        return self.security_notifier.lookup_url

    @property
    def security_notifier(self):
        """Get a local security notifier.

        The security notifier is installed as a local utility by an
        event handler in the security module.
        """
        site = grok.getSite()
        site_manager = site.getSiteManager()
        return site_manager.queryUtility(ISecurityNotifier, default=None)

    @property
    def secnotes_enabled(self):
        if self.security_notifier is None:
            return False
        return self.security_notifier.enabled

    @property
    def secnotes_message(self):
        if self.security_notifier is None:
            return u'Security notifier is not installed.'
        return self.security_notifier.getNotification()

    @property
    def server_control(self):
        return queryUtility(IServerControl)

    @property
    def runtime_info(self):
        try:
            ri = IRuntimeInfo(applicationController)
        except TypeError:
            formatted = dict.fromkeys(self._fields, self._unavailable)
            formatted["Uptime"] = self._unavailable
        else:
            formatted = self._getInfo(ri)

        return formatted

    def _getInfo(self, ri):
        formatted = {}
        for name in self._fields:
            try:
                value = getattr(ri, "get" + name)()
            except ValueError:
                value = self._unavailable
            formatted[name] = value
        formatted["Uptime"] = self._getUptime(ri)
        return formatted

    def _getUptime(self, ri):
        # make a unix "uptime" uptime format
        uptime = int(ri.getUptime())
        minutes, seconds = divmod(uptime, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        return _('${days} day(s) ${hours}:${minutes}:${seconds}',
                 mapping={'days': '%d' % days,
                          'hours': '%02d' % hours,
                          'minutes': '%02d' % minutes,
                          'seconds': '%02d' % seconds})

    @property
    def current_message(self):
        source = getUtility(
          z3c.flashmessage.interfaces.IMessageSource, name='admin')
        messages = list(source.list())
        if messages:
            return messages[0]

    def updateSecurityNotifier(self, setsecnotes=None, setsecnotesource=None,
                               secnotesource=None):
        if self.security_notifier is None:
            site = grok.getSite()
            site_manager = site.getSiteManager()
            if 'grokadmin_security' not in site_manager:
                site_manager['grokadmin_security'] = SecurityNotifier()
                utility = site_manager['grokadmin_security']
                site_manager.registerUtility(
                    utility, ISecurityNotifier, name=u'')

        if setsecnotesource is not None:
            self.security_notifier.setLookupURL(secnotesource)
        if setsecnotes is not None:
            if self.security_notifier.enabled is True:
                self.security_notifier.disable()
            else:
                self.security_notifier.enable()
        if self.secnotes_enabled is False:
            return
        return

    def update(self, time=None, restart=None, shutdown=None,
               setsecnotes=None, secnotesource=None, setsecnotesource=None,
               admin_message=None, submitted=False, dbName="", pack=None,
               days=0):

        # Packing control
        if pack is not None:
            return self.pack(dbName, days)

        # Security notification control
        self.updateSecurityNotifier(setsecnotes, setsecnotesource,
                                    secnotesource)


        if not submitted:
            return

        # Admin message control
        source = getUtility(
          z3c.flashmessage.interfaces.IMessageSource, name='admin')
        if admin_message is not None:
            source.send(admin_message)
        elif getattr(source, 'current_message', False):
            source.delete(source.current_message)

        # Restart control
        if time is not None:
            try:
                time = int(time)
            except:
                time = 0
        else:
            time = 0

        if restart is not None:
            self.server_control.restart(time)
        elif shutdown is not None:
            self.server_control.shutdown(time)

        self.redirect(self.url())

    @property
    def databases(self):
        res = []
        for name, db in getUtilitiesFor(IDatabase):
            d = dict(
                dbName=db.getName(),
                utilName=str(name),
                size=self._getSize(db))
            res.append(d)
        return res

    def _getSize(self, db):
        """Get the database size in a human readable format.
        """
        size = db.getSize()
        if not isinstance(size, (int, float)):
            return str(size)
        return byteDisplay(size)

    def pack(self, dbName, days):
        try:
            days = int(days)
        except ValueError:
            self.flash('Error: Invalid Number')
            return
        db = getUtility(IDatabase, name=dbName)
        print("DB: ", db, days)
        db.pack(days=days)
        return
        try:
            db.pack(days=days)
            self.flash('ZODB `%s` successfully packed.' % (dbName))
        except FileStorageError as err:
            self.flash('ERROR packing ZODB `%s`: %s' % (dbName, err))
