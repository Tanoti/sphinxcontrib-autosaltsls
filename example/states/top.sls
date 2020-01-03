###
# Default top file to run on state.highstate
#
### environment
# Common to all salt environments
base:
  ### topfile_id
  # All minions run these states
  '*': nrpe

  ### topfile_id
  'role:webserver':
    - match: grain
    - roles.webserver

### environment
# Production states only
production:
  ### topfile_id
  'role:proxy':
    - match: grain
    - roles.proxy