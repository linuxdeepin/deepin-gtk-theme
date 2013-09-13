#include <gtk/gtk.h>
#include <gdk/gdkx.h>

GtkWindow* w = NULL;

gboolean update_style()
{
    char* cwd = g_get_current_dir();
    char* path = g_build_filename(cwd, g_get_prgname(), NULL);
    g_free(cwd);

    GAppInfo* info = g_app_info_create_from_commandline(path, g_get_prgname(), G_APP_INFO_CREATE_NONE, NULL);
    g_app_info_launch(info, NULL, NULL, NULL);

    char* cmd = g_strdup_printf("xkill -id %d\n", GDK_WINDOW_XID(gtk_widget_get_window(w)));
    system(cmd);
    g_free(cmd);

    exit(0);
}

void monitor_resource_file()
{
    GFile* css  = g_file_new_for_path("/usr/share/themes/Deepin/gtk-3.0/");
    GFileMonitor* m_css = g_file_monitor_directory(css,  G_FILE_MONITOR_NONE, NULL, NULL);
    g_file_monitor_set_rate_limit(m_css, 200);
    g_signal_connect(m_css, "changed", G_CALLBACK(update_style), NULL);
}

int main()
{
    gtk_init(NULL, NULL);
    monitor_resource_file();
    GtkBuilder* b = gtk_builder_new();
    gtk_builder_add_from_file(b, "theme.ui", NULL);
    w = gtk_builder_get_object(b, "window1");
    gtk_widget_realize(w);
    gdk_window_set_focus_on_map(gtk_widget_get_window(w), FALSE);
    gtk_widget_set_size_request(GTK_WIDGET(w), 400, 500);
    gtk_widget_show_all(w);
    g_signal_connect(w, "destroy", gtk_main_quit, NULL);
    gtk_main();
}
