##############################################################################
#
# Copyright (c) 2007-2008 Zope Corporation and Contributors.
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
"""Views for the grok admin UI"""

import grok
import z3c.flashmessage.interfaces

from grokui.admin.interfaces import ISecurityNotifier
from grokui.admin.utilities import getVersion, getURLWithParams

from ZODB.broken import Broken
from ZODB.interfaces import IDatabase
from BTrees.OOBTree import OOBTree

import zope.component
from zope.interface import Interface
from zope.traversing.browser import absoluteURL
from zope.app.applicationcontrol.interfaces import IServerControl
from zope.app.applicationcontrol.applicationcontrol import applicationController
from zope.app.applicationcontrol.browser.runtimeinfo import RuntimeInfoView
from zope.app.applicationcontrol.browser.zodbcontrol import ZODBControlView
from zope.app.folder.interfaces import IRootFolder
from zope.exceptions import DuplicationError
from ZODB.FileStorage.FileStorage import FileStorageError
from zope.contentprovider.interfaces import IContentProvider

from grokui.base.layout import AdminView
from grokui.base.interfaces import IInstallableApplication, IInstalledApplication, IApplicationRepresentation
  
grok.context(IRootFolder)
grok.templatedir("templates")



class ManageApplications(grok.Permission):
    grok.name('grok.ManageApplications')


class GrokAdminInfoView(grok.View):
    """A base to provide machinereadable views.
    """
    grok.name('grokadmin')
    grok.require('grok.ManageApplications')
    
    def render(self):
        return u'go to @@version or @@secnotes'


class AdminViewBase(grok.View):
    """A grok.View with a special application_url.

    We have to compute the application_url different from common
    grok.Views, because we have no root application object in the
    adminUI. To avoid mismatch, we also call it 'root_url'.

    """
    grok.baseclass()
    
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


class GrokAdminVersion(grok.View):
    """Display version of a package.

    Call this view via http://localhost:8080/@@grokadmin/@@version to
    get the used grok version. Call
    http://localhost:8080/@@grokadmin/@@version?pkg=<pkgname> to get
    the used version of package <pkgname>.
    """
    grok.name('version')
    grok.context(GrokAdminInfoView)
    grok.require('grok.ManageApplications')
    def render(self, pkg='grok'):
        return u'%s %s' % (pkg, getVersion(pkg))


class GrokAdminSecurityNotes(grok.View):
    """Display current security notification.

    Call this view via http://localhost:8080/@@grokadmin/@@secnote
    """
    grok.name('secnote')
    grok.context(GrokAdminInfoView)
    grok.require('grok.ManageApplications')
    def render(self):
        site = grok.getSite()
        site_manager = site.getSiteManager()
        notifier = site_manager.queryUtility(ISecurityNotifier, default=None)
        return notifier.getNotification()


class Add(grok.View):
    """Add an application.
    """

    grok.require('grok.ManageApplications')

    def update(self, inspectapp=None, application=None):
        if inspectapp is not None:
            self.redirect(self.url("docgrok") + "/%s/index"%(
                    application.replace('.','/'),))
        return

    def render(self, application, name, inspectapp=None):
        if name is None or name == "":
            self.redirect(self.url(self.context))
            return
        if name is None or name == "":
            self.redirect(self.url(self.context))
            return
        app = zope.component.getUtility(grok.interfaces.IApplication,
                                        name=application)
        try:
            new_app = app()
            grok.notify(grok.ObjectCreatedEvent(new_app))
            self.context[name] = new_app
            self.flash(u'Added %s `%s`.' % (application, name))
        except DuplicationError:
            self.flash(u'Name `%s` already in use. '
                       u'Please choose another name.' % (name,))
        self.redirect(self.url(self.context))


class ManageApps(grok.View):
    """Manage applications (delete, rename).
    """

    grok.require('grok.ManageApplications')

    def delete(self, items):
        """Delete applications in items.
        """
        msg = u''
        for name in items:
            try:
                del self.context[name]
                msg = (u'%sApplication `%s` was successfully '
                       u'deleted.\n' % (msg, name))
            except AttributeError:
                # Object is broken.. Try it the hard way...
                # TODO: Try to repair before deleting.
                obj = self.context[name]
                if not hasattr(self.context, 'data'):
                    msg = (
                        u'%sCould not delete application `%s`: no '
                        u'`data` attribute found.\n' % (msg, name))
                    continue
                if not isinstance(self.context.data, OOBTree):
                    msg = (
                        u'%sCould not delete application `%s`: no '
                        u'`data` is not a BTree.\n' % (msg, name))
                    continue
                self.context.data.pop(name)
                self.context.data._p_changed = True
                msg = (u'%sBroken application `%s` was successfully '
                       u'deleted.\n' % (msg, name))

        flash(msg)
        self.redirect(self.url(self.context))

    def render(self, rename=None, delete=None, items=None):

        if items is None:
            return self.redirect(self.url(self.context))

        if not isinstance(items, list):
            items = [items]

        if delete is not None:
            return self.delete(items)
        elif rename is not None:
            return self.redirect(getURLWithParams(
                    self.url(self.context, '@@grokadmin_rename'),
                    data=dict(items=items)))
        self.redirect(self.url(self.context))


class Rename(AdminViewBase):
    """Rename Grok applications.
    """
    grok.name('grokadmin_rename')
    grok.template('rename')
    grok.require('grok.ManageApplications')

    def update(self, cancel=None, items=None, new_names=None):
        msg = u''

        if cancel is not None:
            return self.redirect(self.url(self.context))

        if not isinstance(items, list):
            items = [items]
        self.apps = items

        if new_names is not None and len(new_names) != len(items):
            return self.redirect(self.url(self.context))

        if new_names is None:
            return

        mapping = dict([(items[x], new_names[x]) for x in range(len(items))])

        for oldname, newname in mapping.items():
            if oldname == newname:
                continue
            if oldname not in self.context.keys():
                flash('Could not rename %s: not found' % oldname)
                continue
            if newname in self.context.keys():
                flash('`%s` already exists.' % newname)
                continue
            self.context[newname] = self.context[oldname]
            self.context[newname].__name__ = newname
            del self.context[oldname]
            flash('Renamed `%s` to `%s`.' % (oldname, newname))
        self.redirect(self.url(self.context))
        return


class Index(AdminViewBase):
    """A redirector to the real frontpage.
    """
    grok.name('index.html') # The root folder is not a grok.Model
    grok.require('grok.ManageApplications')

    def update(self):
        apps = zope.component.getAllUtilitiesRegisteredFor(
            grok.interfaces.IApplication)
        self.applications = ("%s.%s" % (x.__module__, x.__name__)
                             for x in apps)
        # Go to the first page immediately.
        self.redirect(self.url('applications'))
