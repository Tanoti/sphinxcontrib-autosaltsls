###
# Apache settings for use states
#
apache:
  ### summary_id
  # List of files that should be removed from /etc/httpd/conf.d
  absent_files:
    - autoindex.conf
    - notrace.conf
    - perl.conf
    - userdir.conf
    - welcome.conf
