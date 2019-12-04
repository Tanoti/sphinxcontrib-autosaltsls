###
# Ensure required kernel settings have been made
#
# Update ``/etc/sysctl.conf`` and set kernel.sysrq = 1
kernel_magic_key_enabled:
  file.replace:
    - name: /etc/sysctl.conf
    - pattern: ^#?\s*kernel.sysrq\s*=\s*0
    - repl: kernel.sysrq = 1
    - count: 1
    - append_if_not_found: True
