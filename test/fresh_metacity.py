#! /usr/bin/env python
# -*- coding: utf-8 -*-

import deepin_gsettings

WM_PREFERENCES_CONF = "org.gnome.desktop.wm.preferences"
WM_PREFERENCES_SETTINGS = deepin_gsettings.new(WM_PREFERENCES_CONF)

current_theme = WM_PREFERENCES_SETTINGS.get_string('theme')
if current_theme == 'Deepin':
    WM_PREFERENCES_SETTINGS.set_string('theme', 'Deepin-Dark')
else:
    WM_PREFERENCES_SETTINGS.set_string('theme', 'Deepin')
