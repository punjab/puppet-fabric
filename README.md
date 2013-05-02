# Install puppet on multiple servers using Fabric
This bunch of scripts help automate and install puppet server on multiple servers. 

[Fabric](fabfile.org) being used for installing puppet, which points to puppet server and start taking commands from there.

## Steps
Preferably use Python in [virtualenv](http://pypi.python.org/pypi/virtualenv) using [virtualenvwrapper](www.doughellmann.com/projects/virtualenvwrapper/). It is similar to using [RVM](https://rvm.io/rvm/install/) or [rbenv](https://github.com/sstephenson/rbenv) in Ruby. Else use `sudo` prepend the following command with sudo to install on the default python installation. It assumes you already have Python on your machine.

		pip install -r requirements.txt
		
Now list available fabric commands (similar to `Rakefile -T `in ruby).

		fab -l

If you do not already have generated ssh keys, use the following command. 

		fab generate_keys
		
Now edit the list of server in an array in the fabfile

		env.hosts = ['server1', 'server2']
		
Now run

		fab deploy
		
Sit back with a cup of coffee and see puppet installed on the servers.

