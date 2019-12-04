###
# Auto-accept a minion key
#
# This reactor is run when an 'act' event is seen
#! Internal note: Make sure the reactor is enabled in the config
### summary_id
# Use wheel.key.accept supplying the minion id using jinja
{%- if 'act' in data and data['act'] == 'pend'                %}
minion_add:
  wheel.key.accept:
    - match: {{ data['id'] }}
{%- endif                                                     %}
