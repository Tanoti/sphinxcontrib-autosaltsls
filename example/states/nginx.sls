#!pyobjects
###
# Ensure Nginx proxy has been installed and configured

with Pkg.installed("nginx"):
    Service.running("nginx", enable=True)

    with Service("nginx", "watch_in"):
        File.managed(
            "/etc/nginx/conf.d/proxy.conf",
            owner='root', group='root', mode='0444',
            source='salt://nginx/proxy.conf'
        )