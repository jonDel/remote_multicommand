.. image:: https://readthedocs.org/projects/remote-multicommand/badge/?version=master
   :target: http://remote-multicommand.readthedocs.io/en/master/?badge=master
   :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/jonDel/remote_multicommand/badge.svg?branch=master
   :target: https://coveralls.io/github/jonDel/remote_multicommand?branch=master

.. image:: https://landscape.io/github/jonDel/remote_multicommand/master/landscape.svg?style=flat
    :target: https://landscape.io/github/jonDel/remote_multicommand/master
    :alt: Code Health

.. image:: https://www.versioneye.com/user/projects/582ddf73c8dd3300448f9e81/badge.svg?style=flat
    :target: https://www.versioneye.com/user/projects/582ddf73c8dd3300448f9e81


remote_multicommand
===================

**remote_multicommand** provides execution of multiple commands in multiple servers in parallel (multiple processes)


Executing a list of commands in multiple servers in parallel
------------------------------------------------------------

.. code:: python

  >>> from remote_multicommand import RemoteMultiCommand
  >>> cmds_list = ['hostname','whoami']
  >>> rm_cmd = RemoteMultiCommand('/tmp/sshkey')
  Log: Changing log level to ERROR | Log level:ERROR | Date:01/11/2016 16:40:10
  >>> rm_cmd.set_log_level('DEBUG')
  Log: Changing log level to DEBUG | Log level:DEBUG | Date:01/11/2016 16:40:12
  >>> servers_list = ['serverOne', 'serverTwo', 'serverThree', 'serverFour']
  >>> rm_cmd.launch_list_of_commands(cmds_list, num_of_process, servers_list, ssh_log_level='DEBUG')
  Log: Executing 2 commands in the list of servers: | Log level:INFO | Date:01/11/2016 16:40:27
  Log: Processing in the 4 servers will be done in 1 iterations. | Log level:INFO |
    # Date:01/11/2016 16:40:27
  Log: Processing 4 servers in this iteration. | Log level:DEBUG | Date:01/11/2016 16:40:27
  Log: Servers: ['serverOne', 'serverTwo', 'serverThree', 'serverFour'] | Log level:DEBUG |
    # Date:01/11/2016 16:40:27
  Log: It took 2.338 seconds to execute command 'hostname' in all 4 servers. | Log level:INFO
    # | Date:01/11/2016 16:40:30
  Log: Processing in the 4 servers will be done in 1 iterations. | Log level:INFO |
    # Date:01/11/2016 16:40:30
  Log: Processing 4 servers in this iteration. | Log level:DEBUG | Date:01/11/2016 16:40:30
  Log: Servers: ['serverOne', 'serverTwo', 'serverThree', 'serverFour'] | Log level:DEBUG |
    # Date:01/11/2016 16:40:30
  Log: It took 2.396 seconds to execute command 'whoami' in all 4 servers. | Log level:INFO |
    # Date:01/11/2016 16:40:32
  Log: Server serverTwo:
   - All 2 commands were issued: Yes
   - Number of commands issued: 2
   - Number of commands bypassed: 0 | Log level:INFO | Date:01/11/2016 16:40:32
  Log: Server serverOne:
   - All 2 commands were issued: Yes
  - Number of commands issued: 2
   - Number of commands bypassed: 0 | Log level:INFO | Date:01/11/2016 16:40:32
  Log: Server serverThree:
   - All 2 commands were issued: Yes
    - Number of commands issued: 2
   - Number of commands bypassed: 0 | Log level:INFO | Date:01/11/2016 16:40:32
  Log: Server serverFour:
   - All 2 commands were issued: Yes
   - Number of commands issued: 2
   - Number of commands bypassed: 0 | Log level:INFO | Date:01/11/2016 16:40:32
  Log: It took 4.735 seconds to execute the list of commands in all 4 servers. | Log level:INFO
  | Date:01/11/2016 16:40:32

  {'serverTwo': [OrderedDict([('command', 'hostname'), ('access', True),
  ('result', True), ('output', 'serverTwo\n')]),
  OrderedDict([('command', 'whoami'), ('access', True), ('result', True), ('output', 'root\n')])],
  'serverOne': [OrderedDict([('command', 'hostname'), ('access', True), ('result', True),
  ('output', 'serverOne\n')]),
  OrderedDict([('command', 'whoami'), ('access', True), ('result', True), ('output', 'root\n')])],
  'serverThree': [OrderedDict([('command', 'hostname'), ('access', True), ('result', True),
  ('output', 'serverThree\n')]),
  OrderedDict([('command', 'whoami'), ('access', True), ('result', True), ('output', 'root\n')])],
  'serverFour': [OrderedDict([('command', 'hostname'), ('access', True), ('result', True),
  ('output', 'serverFour\n')]),
  OrderedDict([('command', 'whoami'), ('access', True), ('result', True), ('output', 'root\n')])]}


Installation
------------

To install remote_multicommand, simply run:

::

  $ pip install remote_multicommand

remote_multicommand is compatible with Python 2.6+

Documentation
-------------

https://remote_multicommand.readthedocs.io

Source Code
-----------

Feel free to fork, evaluate and contribute to this project.

Source: https://github.com/jonDel/remote_multicommand

License
-------

GPLv3 licensed.

OBS
---

Due to bug https://github.com/paramiko/paramiko/issues/753, we must use paramiko versions under or equal 1.17.2

