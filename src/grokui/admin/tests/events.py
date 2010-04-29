"""
Events
******

When we create a new app, a grok.IObjectCreatedEvent is called:

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

We fetch the standard page, which should provide us a menu to get all
installable grok applications/components.

  >>> browser.open("http://localhost/")

When we create a new instance of our app, the eventhandler defined
below will be called:

  >>> subform = browser.getForm(name='grokui.admin.tests.events.App')
  >>> subform.getControl(name='name').value = 'my-app'
  >>> subform.getControl('Create').click()
  ObjectCreated event happened.

"""
import grok


class App(grok.Application, grok.Container):
    pass


@grok.subscribe(App, grok.IObjectCreatedEvent)
def handle_my_event(obj, event):
    print "ObjectCreated event happened."
