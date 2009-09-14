##############################################################################
#
# Copyright (c) 2009 Zope Corporation and Contributors.
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
"""
Events
******

When we create a new app, a grok.IObjectCreatedEvent is called:

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  
We fetch the standard page, which should provide us a menu to get all
installable grok applications/components.

  >>> browser.open("http://localhost/")

When we create a new instance of our app, the eventhandler defined
below will be called:

  >>> subform = browser.getForm(name='App')
  >>> subform.getControl('Name your new app:').value = 'my-app'
  >>> subform.getControl('Create').click()
  ObjectCreated event happened.

"""
import grok
from zope.component import interfaces

class App(grok.Application, grok.Container):
    pass

@grok.subscribe(App, grok.IObjectCreatedEvent)
def handle_my_event(obj, event):
    print "ObjectCreated event happened."
