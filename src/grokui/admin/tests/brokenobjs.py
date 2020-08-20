"""
Broken objects management
=========================

The admin-UI now supports detection and deletion of broken objects. It
is still limited to IApplication objects in the root folder. Options
to repair broken objects are also still missing.

We first setup the environment:

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

If no broken applications are in the root, everything should look as
usual:

  >>> browser.open('http://localhost/++grokui++/applications')
  >>> 'Broken applications:' not in browser.contents
  True

We have an application type available, which is intentionally broken
and defined below::

  >>> browser.open('http://localhost/++grokui++/applications')
  >>> 'PseudoBroken' in browser.contents
  True

We add an instance of that new type:

  >>> subform = browser.getForm(
  ...             name='grokui.admin.tests.brokenobjs.PseudoBroken')
  >>> subform
  <zope.testbrowser.browser.Form object at 0x...>

  >>> subform.getControl(name='name').value = 'mybrokenobj'
  >>> subform.getControl('Create').click()

and the broken object should show up in the applications list:

 >>> print(browser.contents)
 <html xmlns="http://www.w3.org/1999/xhtml">
 ...
 ...Currently no working applications are...installed...
 ...
 ...Broken applications:...
 ...
 ...(broken type: grokui.admin.tests.brokenobjs.PseudoBroken)...
 ...This application is broken!...
 ...

If we want to delete the broken object, we can do so:

  >>> ctrl = browser.getControl(name='items')
  >>> ctrl.getControl(value='mybrokenobj').selected = True
  >>> browser.getControl('Delete Selected').click()
  >>> print(browser.contents)
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ...Application `mybrokenobj` was successfully deleted.
  ...

and the 'Broken applications' section won't show up anymore:

  >>> 'Broken applications:' not in browser.contents
  True


"""
import grok
from ZODB.broken import Broken


class PseudoBroken(grok.Application, grok.Container, Broken):
    """A class intentionally broken.
    """
    pass
