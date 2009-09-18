# -*- coding: utf-8 -*-

import grok
import z3c.flashmessage.interfaces

from grokui.base.layout import AdminView
from grokui.admin.interfaces import ISecurityNotifier
from grokui.admin.utilities import getVersion, getURLWithParams

from ZODB.interfaces import IDatabase
from ZODB.FileStorage.FileStorage import FileStorageError

import zope.component
from zope.interface import Interface
from zope.traversing.browser import absoluteURL
from zope.app.applicationcontrol.interfaces import IServerControl
from zope.app.applicationcontrol.browser.runtimeinfo import RuntimeInfoView
from zope.app.applicationcontrol.browser.zodbcontrol import ZODBControlView
from zope.app.applicationcontrol.applicationcontrol import applicationController

grok.templatedir("templates")


class Server(AdminView, ZODBControlView):
    """Zope3 management screen.
    """
    grok.title('Server')
    grok.require('grok.ManageApplications')

    @property
    def grok_version(self):
        return getVersion('grok')

    @property
    def grokuiadmin_version(self):
        return getVersion('grokui.admin')

    def root_url(self, name=None):
        obj = self.context
        result = ""
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
            # Safety belt if installation of notifier failed
            return False
        return self.security_notifier.enabled

    @property
    def secnotes_message(self):
        if self.security_notifier is None:
            return u'Security notifier is not installed.'
        return self.security_notifier.getNotification()
    
    @property
    def server_control(self):
        return zope.component.queryUtility(IServerControl, '', None)

    @property
    def runtime_info(self):
        riv = RuntimeInfoView()
        riv.context = applicationController
        return riv.runtimeInfo()

    @property
    def current_message(self):
        source = zope.component.getUtility(
          z3c.flashmessage.interfaces.IMessageSource, name='admin')
        messages = list(source.list())
        if messages:
            return messages[0]

    def updateSecurityNotifier(self, setsecnotes=None, setsecnotesource=None,
                               secnotesource=None):
        if self.security_notifier is None:
            return
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
        source = zope.component.getUtility(
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

    def pack(self, dbName, days):
        try:
            days = int(days)
        except ValueError:
            flash('Error: Invalid Number')
            return
        db = zope.component.getUtility(IDatabase, name=dbName)
        print "DB: ", db, days
        db.pack(days=days)
        return
        try:
            db.pack(days=days)
            flash('ZODB `%s` successfully packed.' % (dbName))
        except FileStorageError, err:
            flash('ERROR packing ZODB `%s`: %s' % (dbName, err))