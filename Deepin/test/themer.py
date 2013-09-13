#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import os
import logging

UI_FILE = "preview.ui"

def walk_directories(dirs, filter_func):
    valid = []
    try:
        for thdir in dirs:
            if os.path.isdir(thdir):
                for t in os.listdir(thdir):
                    if filter_func(os.path.join(thdir, t)):
                         valid.append(t)
    except:
        logging.critical("Error parsing directories", exc_info=True)
    return valid

def build_combo_box_text(combo, selected, values):
    """
    builds a GtkComboBox and model containing the supplied values.
    @values: a list of 2-tuples (value, name)
    """
    store = Gtk.ListStore(str, str)
    store.set_sort_column_id(0, Gtk.SortType.ASCENDING)

    selected_iter = None
    for (val, name) in values:
        _iter = store.append( (val, name) )
        if val == selected:
            selected_iter = _iter

    combo.set_model(store)
    renderer = Gtk.CellRendererText()
    combo.pack_start(renderer, True)
    combo.add_attribute(renderer, 'markup', 1)
    if selected_iter:
        combo.set_active_iter(selected_iter)

def make_combo_list_with_default(opts, default, title=True, default_text=None):
    """
    Turns a list of values into a list of value,name (where name is the
    display name a user will see in a combo box). If a value is opt is
    equal to that supplied in default the display name for that value is
    modified to "value <i>(default)</i>"

    @opts: a list of value
    @returns: a list of 2-tuples (value, name)
    """
    themes = []
    for t in opts:
        if t.lower() == "default" and t != default:
            #some themes etc are actually called default. Ick. Dont show them if they
            #are not the actual default value
            continue

        if title and len(t):
            name = t[0].upper() + t[1:]
        else:
            name = t

        if t == default:
            #indicates the default theme, e.g Adwaita (default)
            name = default_text or "%s <i>(default)</i>" % name

        themes.append((t, name))
    return themes

class Window():
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        #self.builder.connect_signals(self)
        
        self.window = self.builder.get_object("window")
        self.window.connect("destroy", Gtk.main_quit)
        
        self.default_settings = Gtk.Settings.get_default()
        
        #print self.default_settings.get_property("gtk-theme-name")
        #self.default_settings.set_property("gtk-theme-name", "Adwaita")
        self.combo = self.builder.get_object("themes_combobox")
        
        themes_list = make_combo_list_with_default(self._get_valid_themes(), "Adwaita")
        current_theme_color = self.default_settings.get_property("gtk-theme-name")
        
        build_combo_box_text(self.combo, current_theme_color, themes_list)
        self.combo.connect('changed', self._on_combo_changed)
        self.window.show_all()
        Gtk.main()
        
    def _get_valid_themes(self):
        """ Only shows themes that have variations for gtk+-3 and gtk+-2 """
        dirs = ( os.path.join("/usr/share", "themes"),
                 os.path.join(os.path.expanduser("~"), ".themes"))
        valid = walk_directories(dirs, lambda d:
                    os.path.exists(os.path.join(d, "gtk-2.0")) and \
                        os.path.exists(os.path.join(d, "gtk-3.0")))
        return valid
        
    def _on_combo_changed(self, combo):
        _iter = combo.get_active_iter()
        if _iter:
            value = combo.get_model().get_value(_iter, 0)
            self.default_settings.set_property("gtk-theme-name", value)

if __name__ == "__main__":
    win = Window()
