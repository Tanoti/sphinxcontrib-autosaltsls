###
# Template state file
#
# It should not be processed any further for documentation purposes
### ignore
# Make sure all included states are at the top of the file here
include:
  - some_state

# We always use a state ID and it should be in the past tense (i.e. assert that something has happened)
state_id_in_past_tense:
  <state>.<method>:
    - name: something
    ...