.. image:: https://readthedocs.org/projects/remotemulticommand/badge/?version=master
   :target: http://remotemulticommand.readthedocs.io/en/master/?badge=master
   :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/jonDel/remoteMultiCommand/badge.svg?branch=master
   :target: https://coveralls.io/github/jonDel/remoteMultiCommand?branch=master

.. image:: https://landscape.io/github/jonDel/remoteMultiCommand/master/landscape.svg?style=flat
    :target: https://landscape.io/github/jonDel/remoteMultiCommand/master
    :alt: Code Health

.. image:: https://www.versioneye.com/user/projects/582340127a72950047198059/badge.svg?style=flat
    :target: https://www.versioneye.com/user/projects/582340127a72950047198059


remoteMultiCommand
==================

**remoteMultiCommand** provides execution of multiple commands in multiple servers in parallel (multiple processes)


Executing a list of commands in multiple servers in parallel
------------------------------------------------------------

.. code:: python

  >>> from remoteMultiCommand import remoteMultiCommand
  >>> cmdsList = ['hostname','whoami']
  >>> rmCmd = remoteMultiCommand('/tmp/sshkey')
  Log: Changing log level to ERROR | Log level:ERROR | Date:01/11/2016 16:40:10
  >>> rmCmd.set_log_level('DEBUG')
  Log: Changing log level to DEBUG | Log level:DEBUG | Date:01/11/2016 16:40:12
  >>> serversList = ['serverOne', 'serverTwo', 'serverThree', 'serverFour']
  >>> rmCmd.launchListOfCommands(cmdsList, numOfProcess, serversList, sshLogLevel='DEBUG')
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

To install remoteMultiCommand, simply run:

::

  $ pip install remoteMultiCommand

remoteMultiCommand is compatible with Python 2.6+

Documentation
-------------

https://remoteMultiCommand.readthedocs.io

Source Code
-----------

Feel free to fork, evaluate and contribute to this project.

Source: https://github.com/jonDel/remoteMultiCommand

License
-------

GPLv3 licensed.

OBS
---

Due to bug https://github.com/paramiko/paramiko/issues/753, we must use paramiko versions under or equal 1.17.2

