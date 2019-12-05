###
# Auto-accept a minion key
#
# This reactor is run when an 'act' event is seen
#! Internal note: Make sure the reactor is enabled in the config
{%- if 'act' in data and data['act'] == 'pend' %}
### summary_id
# Use wheel.key.accept supplying the minion id using jinja
minion_add:
  wheel.key.accept:
    - match: {{ data['id'] }}
{%- endif %}
