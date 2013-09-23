#include <gtk/gtk.h>

GtkWindow* w = NULL;

gboolean update_style()
{
    system("killall "APP_NAME);

    GAppInfo* info = g_app_info_create_from_commandline(APP_NAME, APP_NAME, G_APP_INFO_CREATE_NONE, NULL);
    g_app_info_launch(info, NULL, NULL, NULL);
}

void monitor_resource_file()
{
    GFile* css  = g_file_new_for_path("/usr/share/themes/Deepin/gtk-3.0/");
    GFile* apps = g_file_new_for_path("/usr/share/themes/Deepin/gtk-3.0/apps");

    GFileMonitor* m_css = g_file_monitor_directory(css,  G_FILE_MONITOR_NONE, NULL, NULL);
    GFileMonitor* m_apps = g_file_monitor_directory(apps,  G_FILE_MONITOR_NONE, NULL, NULL);
    g_file_monitor_set_rate_limit(m_css, 200);
    g_file_monitor_set_rate_limit(m_apps, 200);
    g_signal_connect(m_css, "changed", G_CALLBACK(update_style), NULL);
    g_signal_connect(m_apps, "changed", G_CALLBACK(update_style), NULL);
}

int main()
{
    gtk_init(NULL, NULL);
    monitor_resource_file();
    gtk_main();
}
