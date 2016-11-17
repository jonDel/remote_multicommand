import time
from collections import OrderedDict
from copy import copy
from loggers import Loggers
from pathos.multiprocessing import ProcessingPool as Pool
from ssh_paramiko import ssh_paramiko

class RemoteMultiCommand(Loggers):
    '''Execute commands in parallel in remote servers

    Provides a layer of abstraction for executing multiple commands in multiple servers
        with multiple processes in parallel

    Arguments:
        keySSH(:obj:`str`): path of the ssh private key to connect (must be None if using user
            and pasword to connect)
        logFolder(:obj:`str`, **optional** , *default* =None): folder where the log files of
            this class will be generated
        username(:obj:`str`, *optional* , *default* =root):  username using the connection
        password(:obj:`str`,optional, *default* =None):  password for connection if using user
            and password instead of key
        sshPort(:obj:`str`, optional, *default* =22):  ssh tcp port
        serverHasDns(:obj:`bool`, optional, *default* =True): if the server is not registered
            in a DNS domain and/or has not its DNS name equals to its hostname, this flag must
            de set to False, otherwise this condition will be checked to certify we are trully
            connected to the right server.

    '''
    def __init__(self, ssh_key, **kwargs):
        self.cmd = None
        self.ssh_key_path = ssh_key
        self.servers_cmd_dict = {}
        self.ssh_log_level = 'ERROR'
        self.ssh_opt_args = kwargs
        self.ssh = ssh_paramiko.RemoteServer(self.ssh_key_path, **self.ssh_opt_args)
        self.ssh.set_log_level(self.ssh_log_level)
        if 'logFolder' in kwargs:
            super(RemoteMultiCommand, self).__init__('RemoteMultiCommand',
                                                     logFolder=kwargs['logFolder'])
        else:
            super(RemoteMultiCommand, self).__init__('RemoteMultiCommand')

    def execute_command(self, server):
        ''' Execute a command in a remote server

        Issues a command in the server and updates the dictionary self.servers_cmd_dict,
        which maintains the state of all commands executed in this object

        Arguments:
            server (:obj:`str`): server where the command will be executed

        Returns:
            dictionary containing the server, the command executed, the result of the
            connection attempt and the result of the command issued

        '''
        ret, output_msg = self.ssh.connect_server(server, False)
        if ret:
            cmd_ret, std_out, std_error = self.ssh.execute_cmd(self.cmd)
            self.ssh.close_connection()
            if cmd_ret:
                std = std_out
            else:
                self.log.error('Error executing command: "'+self.cmd+'" in server '+server
                               +' :'+std_error)
                std = std_error
        else:
            cmd_ret = ret
            std = output_msg
            if not output_msg == 'Host is not registered in DNS domain':
                # Need to reinstantiate the class in this cases
                self.ssh = ssh_paramiko.RemoteServer(self.ssh_key_path, **self.ssh_opt_args)
                self.ssh.set_log_level(self.ssh_log_level)
                self.log.error('Cannot connect to server '+server+' :'+output_msg)
        cmd_dict = OrderedDict()
        cmd_dict['command'] = self.cmd
        cmd_dict['access'] = ret
        cmd_dict['result'] = cmd_ret
        cmd_dict['output'] = std
        return {server:cmd_dict}

    def launch_multicommand(self, cmd, num_of_process, servers_list, ssh_log_level='CRITICAL'):
        '''Launches several processes that execute the command in a list of servers

        Arguments:
            cmd (:obj:`str`): command to be executed in each server of the list
            num_of_process (:obj:`int`): number of separated process launched in each iteration
            servers_list (:obj:`list`): servers list
            ssh_log_level (:obj:`str`, *default* = 'CRITICAL'): log level of the ssh connection.
                Could be 'DEBUG', 'INFO', 'ERROR' or 'CRITICAL'

        Returns:
            servers_cmd_dict (:obj:`dict`): dictionary containing the servers and the result of
                the command

        '''
        self.ssh_log_level = ssh_log_level
        cmd_servers_dict = {}
        num_of_servers = len(servers_list)
        if num_of_process > num_of_servers:
            num_of_process = num_of_servers
        numb_of_iterations, servers_left = divmod(num_of_servers, num_of_process)
        start = time.time()
        counter = 0
        self.cmd = cmd
        self.log.info('Processing in the '+str(num_of_servers)+' servers will be done in '
                      +str(numb_of_iterations+(0 if servers_left == 0 else 1))+' iterations.')
        for iter_num in range(0, num_of_servers, num_of_process):
            self.log.debug('Processing '+str(len(servers_list[iter_num:iter_num+(num_of_process)]))
                           +' servers in this iteration.')
            self.log.debug('Servers: '+str(servers_list[iter_num:iter_num+(num_of_process)]))
            pool = Pool(num_of_process)
            result = pool.map(self.execute_command,
                              servers_list[iter_num:iter_num+(num_of_process)])
            for server_results in result:
                for server, cmd_results in server_results.iteritems():
                    cmd_servers_dict[server] = cmd_results
                    if not server in self.servers_cmd_dict:
                        self.servers_cmd_dict[server] = []
                    self.servers_cmd_dict[server].append(cmd_results)
            counter = counter+num_of_process
            servers_to_process = num_of_servers - counter
            if not servers_to_process <= 0:
                self.log.debug('Still has '+str(num_of_servers-counter)+' servers to process...')
        self.log.info("It took "+str(round(time.time()-start, 3))+" seconds to execute command '"
                      +cmd+"' in all "+str(num_of_servers)+" servers.")
        return cmd_servers_dict

    def launch_list_of_commands(self, script_cmds, num_of_process, servers_list,
                                ssh_log_level='CRITICAL'):
        ''' Launch a list of parallel commands

        Launches several processes that execute a sequence of commands in a list of servers
        For each server, the next commands will only be executed if the preceding command was
        successfull.

        Arguments:
            script_cmds (:obj:`str` or :obj:`list`): list or string containing the commands
                (interprets ";", new line character and comments)
            num_of_process: (:obj:`int`) number of separated process launched in each iteration
            servers_list (:obj:`list`): servers list
            ssh_log_level (:obj:`str`, *default* = 'CRITICAL'): log level of the ssh connection.
                Could be 'DEBUG', 'INFO', 'ERROR' or 'CRITICAL'

        Returns:
            servers_cmd_dict (:obj:`dict`): dictionary containing the servers and the result of
                the command

        '''
        start = time.time()
        self.servers_cmd_dict = {}
        num_of_servers = len(servers_list)
        servers_list_temp = copy(servers_list)
        if type(script_cmds).__name__ != 'list':
            # Turn script_cmds into a list
            script_cmds = script_cmds.replace(';', '\n')
            cmds_list = script_cmds.split('\n')
        else:
            cmds_list = script_cmds
        # Filter null elements and commented lines
        cmds_list = filter(lambda x: x, cmds_list)
        cmds_list = filter(lambda x: x[0] != '#', cmds_list)
        self.log.info('Executing '+str(len(cmds_list))+' commands in the list of servers:')
        for cmd in cmds_list:
            if servers_list_temp:
                result_dict = self.launch_multicommand(cmd, num_of_process,
                                                       servers_list_temp, ssh_log_level)
                for server, results in result_dict.iteritems():
                    if not results['result']:
                        # If this command fails, we remove the server from list
                        servers_list_temp.remove(server)
                        self.log.error('Command "'+cmd+'" returned error. Removing server '
                                       +server+' from execution list')
        for server, result_dict in self.servers_cmd_dict.iteritems():
            log_message = 'Server '+server+':'
            log_message = log_message+'\n - All '+str(len(cmds_list))+' commands were issued: '\
                         +('Yes' if len(result_dict) == len(cmds_list) else 'No')
            log_message = log_message+'\n - Number of commands issued: '+str(len(result_dict))
            log_message = log_message+'\n - Number of commands bypassed: '\
                         +str(len(cmds_list) - len(result_dict))
            self.log.info(log_message)
        self.log.info("It took "+str(round(time.time()-start, 3))+" seconds to execute the list \
                      of commands in all "+str(num_of_servers)+" servers.")
        return self.servers_cmd_dict
