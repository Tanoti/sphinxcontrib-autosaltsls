###
# Ensure the Apache instance is running
#
# This state makes use of pillar data in :pillar:`apache`

### step
# Remove deprecated conf files
#
# The list of files comes from pillar ``apache:absent_files``
{%- set files = salt.pillar.get('apache:absent_files') %}
{%- for file in files %}
apache_config_{{ file }}_removed:
  file.absent:
    - name: /etc/httpd/conf.d/{{ file }}
    - watch_in:
      - service: apache_running
{%- endfor %}

### step_id
# Check the syntax is OK
apache_config_syntax_checked:
  cmd.run:
    - name: httpd -t

### step_id
# Apache running
apache_running:
  service.running:
    - name: httpd
    - enable: true
    - require:
      - cmd: apache_config_syntax_checked