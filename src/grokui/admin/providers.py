# -*- coding: utf-8 -*-

import grok
from grokui.admin import representation


class ApplicationInformation(grok.ViewletManager):
    grok.name('grokui_admin_appinfo')
    grok.context(representation.IApplicationRepresentation)
