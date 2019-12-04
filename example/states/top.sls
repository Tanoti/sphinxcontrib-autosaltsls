###
# Default top file to run on state.highstate
#
'*':
  - nrpe

'role:webserver':
  - match: grain
  - roles.webserver