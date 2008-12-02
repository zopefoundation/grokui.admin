##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
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

Create a mammoth-manager, and stuff it with data which can be packed.
  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open("http://localhost/")
  >>> subform = browser.getForm(name='StuffedMammoth')
  >>> subform.getControl('Name your new app:').value = 'my-stuffed-mammoth'
  >>> subform.getControl('Create').click()

  >>> mylink = browser.getLink('my-stuffed-mammoth (StuffedMammoth)').click()

Stuff this mammoth.
  >>> url = browser.url
  >>> browser.open(url+"?stuffing=fresh+vegetables")
  >>> print browser.contents
  Today's meal is stuffed mammoth!

Time to pull the stuffing out again.
  >>> browser.open(url)
  >>> print browser.contents
  Time to stuff a mammoth!

Check the size of the ZODB.
  >>> browser.open("http://localhost/server")
  >>> lines = [ l.strip() for l in browser.contents.split('\\n') ]
  >>> zodb_size = lines[lines.index("Demo storage 'unnamed'")+  1]
  >>> num_zodb_size = int(zodb_size.split(' ')[0])

Now, pack the database.
  >>> ctrl = browser.getControl(name='pack').click()
  >>> lines = [ l.strip() for l in browser.contents.split('\\n') ]
  >>> zodb_size = lines[lines.index("Demo storage 'unnamed'")+  1]
  >>> new_num_zodb_size = int(zodb_size.split(' ')[0])

Ensure that it is smaller now:
  >>> new_num_zodb_size < num_zodb_size
  True

And clean up after ourselves.
  >>> browser.open("http://localhost/applications")
  >>> ctrl = browser.getControl(name='items')
  >>> ctrl.getControl(value='my-stuffed-mammoth').selected = True
  >>> browser.getControl('Delete Selected').click()

"""

import grok

class StuffedMammoth(grok.Application, grok.Container):
    """A stuffed mammoth"""
    stuffing = None

class Index(grok.View):#

    def update(self, stuffing=None):
        if stuffing is not None:
            self.context.stuffing = stuffing*1000
        else:
            self.context.stuffing = None

    def render(self):
        if self.context.stuffing is None:
            return u"Time to stuff a mammoth!"
        else:
            return u"Today's meal is stuffed mammoth!"
