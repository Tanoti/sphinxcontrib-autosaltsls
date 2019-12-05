###
# Ensure the 'webserver' role has been configured
#
### include
include:
  - apache

### step_id
# Deploy the webserver content after Apache has been installed
webserver_content_deployed:
  file.managed:
    - name: /var/www/html/index.html
    - source: salt::/data/webserver/index.html
    - user: apache
    - group: apache
    - mode: 0644
    - require:
        sls: apache