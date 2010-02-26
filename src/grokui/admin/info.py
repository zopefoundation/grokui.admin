# -*- coding: utf-8 -*-

import grok
from grokui.base import BasePluginInfo
from grokui.admin import utilities
from grokui.admin.security import MSG_DISABLED
from grokui.admin.interfaces import ISecurityNotifier
from zope.component import queryUtility


class AdminInfo(BasePluginInfo):
    grok.name('admin')

    title = u'Applications manager'
    description = (u'This module allows you to create and'
                   u' manage your Grok applications.')

    @property
    def version(self):
        return self.getVersion('grokui.admin')

    def getVersion(self, pkg='grok'):
        return u'%s %s' % (pkg, utilities.getVersion(pkg))

    def getSecurityNotes(self):
        notifier = queryUtility(ISecurityNotifier, default=None)
        if notifier is not None:
            return notifier.getNotification()
        return MSG_DISABLED


class Version(grok.View):
    """Display version of a package.

    Call this view via http://localhost:8080/@@admin/@@version to
    get the used grok version. Call
    http://localhost:8080/++grokui++/++info++admin++/version?pkg=<pkgname>
    or http://localhost:8080/++grokui++/++info++admin++/version/<pkgname>
    to get the used version of package <pkgname>.
    """
    grok.context(AdminInfo)
    grok.require('grok.ManageApplications')

    def publishTraverse(self, request, name):
        self.request.form['pkg'] = name
        return self

    def render(self, pkg='grok'):
        return self.context.getVersion(pkg)


class SecurityNotes(grok.View):
    """Display current security notification.

    Call this view via http://localhost:8080/++grokui++/@@admin/@@secnote
    """
    grok.name('secnote')
    grok.context(AdminInfo)
    grok.require('grok.ManageApplications')

    def render(self):
        return self.context.getSecurityNotes()
