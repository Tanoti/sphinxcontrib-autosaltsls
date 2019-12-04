###
# Ensure nrpe is installed
#
### step_id
nrpe_installed:
  pkg.installed:
    - name: nrpe

### step_id
# Deploy the nrpe.cfg file and set ownership to root:root
nrpe_config_deployed:
  file.managed:
    - name: /etc/nrpe.cfg
    - source: salt://data/nrpe/nrpe.cfg
    - user: root
    - group: root
    - mode: 0644
    - require:
      - pkg: nrpe_installed

### step_id
# Start the service and enable at boot time
nrpe_running:
  service.running:
    - name: nrpe
    - enable: true
    - watch:
      - file: nrpe_config_deployed