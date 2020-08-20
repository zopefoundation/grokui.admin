"""
Events
******

When we create a new app, a grok.IObjectCreatedEvent is called:

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

We fetch the standard page, which should provide us a menu to get all
installable grok applications/components.

  >>> browser.open("http://localhost/")

When we create a new instance of our app, the eventhandlers defined
below will be called:

  >>> subform = browser.getForm(name='grokui.admin.tests.events.App')
  >>> subform.getControl(name='name').value = 'my-app'
  >>> subform.getControl('Create').click()
  ObjectCreated event happened.
  ApplicationAdded event happened.

While the first event (of type `grok.ObjectCreatedEvent`) tells us
that an application was created (but might not be completely
initialized by this time with regard to catalogs and IntIds, the
second event (of type `grok.ApplicationInitializedEvent`) is fired,
when the application is completely ready for use.

"""
import grok


class App(grok.Application, grok.Container):
    pass


@grok.subscribe(App, grok.IObjectCreatedEvent)
def handle_my_event(obj, event):
    print("ObjectCreated event happened.")


@grok.subscribe(App, grok.ApplicationAddedEvent)
def handle_app_initialized_event(obj, event):
    print("ApplicationAdded event happened.")
