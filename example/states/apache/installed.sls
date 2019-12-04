###
# Ensure the Apache instance is installed
#
# Install the Apache package and deploy some configuration files
### step_id
apache_package_installed:
  pkg.installed:
    - name: httpd

### step_id
apache_config_deployed:
  file.managed:
    - name: /etc/httpd/conf/httpd.conf
    - user: root
    - group: root
    - mode: 0644
    - require:
        pkg: apache_package_installed
    - watch_in:
      - sls: apache.running