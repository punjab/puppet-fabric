from __future__ import with_statement
from fabric.api import *
from fabric.contrib.files import exists

# Modify servers on line 47 and line 55 before using

env.use_ssh_config = True # read ~/.ssh/.sshconfig
# env.hosts = ['server1', 'server2']

code_dir = '/tmp'
fname = 'install_puppet_on_rhel.sh'

# Key distribution and management
def generate_keys():
  """ Generate an SSH key to be used for password-less control """
  local("ssh-keygen -N '' -q -t rsa -f ~/.ssh/id_rsa")

@task
def distribute_keys():
  """ Distribute keys to servers """
  local("ssh-copy-id -i ~/.ssh/id_rsa.pub %s@%s" % (env.user, env.host))
  
# Remote Actions
def copy():
  """ Copy puppet installation file to the server. """
  with cd(code_dir):
    if exists(fname):
      run("rm -rf %s" % fname)
    put("%s" % fname, "/tmp/%s" % fname)

def install():
  """ Run installer """
  with cd(code_dir):
    run("chmod +x %s" % fname)
    sudo("./%s" % fname)
    
def permit_selinux():
  """ Temporaily put selinux in permissive mode"""
  sudo("setenforce 0")

def enforce_selinux():
  """ Enforce selinux """
  sudo("setenforce 1")
    
def puppet_run(hostn=''):
  """ Run puppet once"""
  with cd(code_dir):
    sudo("puppet agent apply --server=puppetserver.example.com --no-daemonize --verbose --onetime")
    #sudo("puppet agent apply")
    
def open_port(number, protocol='tcp'):
    """ Open a given port in the firewall"""
    # Get the line before the rule thar rejects ALL
    line = sudo('iptables --line-numbers -vnLRH-Firewall-1-INPUT | grep REJECT | awk \'{print $1}\'')
    # Insert the new rule in that line pushing that line to the next line
    sudo('iptables -I RH-Firewall-1-INPUT %(line)s -s xxx.xxx.x.xxx -p %(protocol)s --dport %(number)s -j ACCEPT' % {'number': number, 'protocol': protocol, 'line': line})
    sudo('service iptables save')
    sudo('service iptables restart')
    
@task
def restart_zabbix():
    """restart zabbix with new configuration"""
    sudo('killall zabbix_agentd')
    run('sleep 5')
    sudo('/usr/local/sbin/zabbix_agentd -c /usr/local/etc/zabbix_agentd.conf')

def clean():
  """ Remove installer file. Add success.txt file in /tmp directory"""
  with cd(code_dir):
    if exists(fname):
      run("rm -rf %s" % fname)
      run('echo "Puppet Installed." > /tmp/success.txt')
      run('date > /tmp/success.txt')

@task      
def deploy():
  """ * Deploy unless success.txt exists. You should only run this. """
  with cd(code_dir):
    distribute_keys()
    if not exists('success.txt'):
      copy()
      install()
      open_port(10050)
      puppet_run()
      clean()
      restart_zabbix()
    else:
      print("Aborting. The success.txt file already exists in /tmp.")
