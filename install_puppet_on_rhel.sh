#!/bin/sh
#
# This script installs puppet on RHEL
# Arvinder Kang

# Check OS and Version
if [ -f /etc/redhat-release ]; then
  a=`grep -i 'red.*hat.*enterprise.*linux' /etc/redhat-release`
  if test $? = 0; then
    DISTRIBUTION=rhel
    VERSION=`cat /etc/redhat-release | sed -e 's#[^0-9]##g' -e 's#7[0-2]#73#'`
    # echo ${DISTRIBUTION} ${VERSION}
  else
    DISTRIBUTION="You are using CentOS, Fedora or some variation of RHEL. Not supported! Surprise!"
    echo $DISTRIBUTION
    exit 1
  fi
else
  DISTRIBUTION="This script only supports RHEL - Version 5.8 and 6.3 specifically. No guarantees otherwise."
  echo $DISTRIBUTION
  exit 1
fi

# Lets Install
cd /tmp/

if [ $VERSION -ge '50' ] && [ $VERSION -le '60' ] ; then
  #echo 'Version 5.x'
  sudo rpm -ivh http://yum.puppetlabs.com/el/5/products/i386/puppetlabs-release-5-6.noarch.rpm
elif [ $VERSION -ge '60' ]; then
  #echo 'Version 6.x'
  sudo rpm -ivh http://yum.puppetlabs.com/el/6/products/i386/puppetlabs-release-6-6.noarch.rpm
else
  echo 'Version other than RHEL 5.8 or 6.3. Now is the time to work on this script!'
  exit 1
fi

sudo yum -y install puppet
