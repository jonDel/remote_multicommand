#!/usr/bin/python -OO
#coding: utf-8
from sshParamiko import sshParamiko
from loggers import Loggers
import time
from pathos.multiprocessing import ProcessingPool as Pool
from collections import OrderedDict
from copy import copy

class remoteMultiCommand(Loggers):
	'''
	Description: provides a layer of abstraction for executing multiple commands in multiple servers
		with multiple processes in paralel
	Arguments:
		Mandatory:
			keySSH: path of the ssh private key to connect (must be None if using user and password to connect)
		Optional:
			logFolder: folder where the log files of this class will be generated (Default: None)
			username:  username using the connection (Default: root)
			password:  password for connection if using user and password instead of key (Default: None)
			sshPort:  ssh tcp port (Default: 22)
			serverHasDns: if the server is not registered in a DNS domain and/or has not its DNS name equals to
				its hostname, this flag must de set to False, otherwise this condition will be checked to certify
	'''
	def __init__(self, sshKey, **kwargs):
		self.sshKeyPath = sshKey
		self.serversCmdDict = {}
		self.sshLogLevel = 'ERROR'
		self.sshOptArgs  = kwargs
		self.ssh = sshParamiko.RemoteServer(self.sshKeyPath, **self.sshOptArgs)
		self.ssh.setLogLevel(self.sshLogLevel)
		if 'logFolder' in kwargs:
			super(remoteMultiCommand, self).__init__('remoteMultiCommand',logFolder=kwargs['logFolder'])
		else:
			super(remoteMultiCommand, self).__init__('remoteMultiCommand')

	def executeCommand(self, server):
		'''
		Description: issues a command in the server and updates the dictionary self.serversCmdDict,
			which maintains the state of all commands executed in this object
		Arguments:
			server: server where the command will be executed
		Return:
			{server:cmdDict}: dictionary containing the server, the command executed, the result of the
				connection attempt and the result of the command issued
		'''
		ret, outputMsg = self.ssh.connectServer(server, False)
		if ret:
			cmdRet,stdOut,stdError = self.ssh.executeCmd(self.cmd);
			self.ssh.closeConnection()
			if cmdRet:
				std=stdOut
			else:
				self.log.error('Error executing command: "'+self.cmd+'" in server '+server+' :'+stdError)
				std=stdError
		else:
			cmdRet = ret
			std = outputMsg
			if not outputMsg == 'Host is not registered in DNS domain':
				# Need to reinstantiate the class in this cases
				self.ssh = sshParamiko.RemoteServer(self.sshKeyPath, **self.sshOptArgs)
				self.ssh.setLogLevel(self.sshLogLevel)
				self.log.error('Cannot connect to server '+server+' :'+outputMsg)
		cmdDict = OrderedDict()
		cmdDict['command']=self.cmd
		cmdDict['access']=ret
		cmdDict['result']=cmdRet
		cmdDict['output']=std
		return {server:cmdDict}

	def launchMultiCommand(self,cmd, numOfProcess,serversList, sshLogLevel='CRITICAL'):
		'''
		Description: launches several processes that execute the command in a list of servers
		Arguments:
			cmd: command to be executed in each server of the list
			numOfProcess: number of separated process launched in each iteration
			serversList: servers list
			sshLogLevel: log level of the ssh connection (default: 'CRITICAL'). Could be 'DEBUG', 'INFO', 'ERROR' or 'CRITICAL'
		Return:
			serversCmdDict: dictionary containing the servers and the result of the command
		'''
		self.sshLogLevel = sshLogLevel
		cmdServersDict = {}
		numOfServers = len(serversList)
		if numOfProcess > numOfServers: numOfProcess = numOfServers
		numbOfIterations, serversLeft = divmod(numOfServers, numOfProcess)
		start=time.time()
		counter = 0
		self.cmd = cmd
		self.log.info('Processing in the '+str(numOfServers)+' servers will be done in '+str(numbOfIterations+(0 if serversLeft == 0 else 1))+' iterations.')
		for iterNum in range(0,numOfServers, numOfProcess):
			self.log.debug( 'Processing '+str(len(serversList[iterNum:iterNum+(numOfProcess)]))+' servers in this iteration.')
			self.log.debug( 'Servers: '+str(serversList[iterNum:iterNum+(numOfProcess)]))
			pool = Pool(numOfProcess)
			result=pool.map(self.executeCommand, serversList[iterNum:iterNum+(numOfProcess)])
			for serverResults in result:
				for server, cmdResults in serverResults.iteritems():
					cmdServersDict[server] = cmdResults
					if not server in self.serversCmdDict:
						self.serversCmdDict[server] = []
					self.serversCmdDict[server].append(cmdResults)
			counter =counter +numOfProcess
			serversToProcess = numOfServers -counter
			if not serversToProcess <= 0: self.log.debug('Still has '+str(numOfServers-counter)+' servers to process...')
		self.log.info("It took "+str(round(time.time()-start,3))+" seconds to execute command '"+cmd+"' in all "+str(numOfServers)+" servers.")
		return cmdServersDict

	def launchListOfCommands(self,scriptCmds,numOfProcess,serversList,sshLogLevel='CRITICAL'):
		'''
		Description: launches several processes that execute a sequence of commands in a list of servers
			For each server, the next commands will only be executed if the preceding command was successfull.
		Arguments:
			scriptCmds: list or string containing the commands (interprets ";", new line character and comments)
			numOfProcess: number of separated process launched in each iteration
			serversList: servers list
			sshLogLevel: log level of the ssh connection (default: 'CRITICAL'). Could be 'DEBUG', 'INFO', 'ERROR' or 'CRITICAL'
		Return:
			serversCmdDict: dictionary containing the servers and the result of the commands
		'''
		start=time.time()
		self.serversCmdDict = {}
		numOfServers = len(serversList)
		serversListTemp  = copy(serversList)
		if type(scriptCmds).__name__ != 'list':
			# Turn scriptCmds into a list
			scriptCmds = scriptCmds.replace(';','\n')
			cmdsList = scriptCmds.split('\n')
		else:
			cmdsList = scriptCmds
		# Filter null elements and commented lines
		cmdsList = filter(lambda x:x, cmdsList)
		cmdsList = filter(lambda x:x[0] != '#', cmdsList)
		self.log.info('Executing '+str(len(cmdsList))+' commands in the list of servers:')
		for cmd in cmdsList:
			if serversListTemp:
				resultDict = self.launchMultiCommand(cmd, numOfProcess,serversListTemp,sshLogLevel)
				for server,results in resultDict.iteritems():
					if not results['result']:
						# If this command fails, we remove the server from list
						serversListTemp.remove(server)
						self.log.error('Command "'+cmd+'" returned error. Removing server '+server+' from execution list')
		for server, resultDict in self.serversCmdDict.iteritems():
			logMessage = 'Server '+server+':'
			logMessage = logMessage+'\n - All '+str(len(cmdsList))+' commands were issued: '+('Yes' if len(resultDict) == len(cmdsList) else 'No')
			logMessage = logMessage+'\n - Number of commands issued: '+str(len(resultDict))
			logMessage = logMessage+'\n - Number of commands bypassed: '+str(len(cmdsList) - len(resultDict))
			self.log.info(logMessage)
		self.log.info("It took "+str(round(time.time()-start,3))+" seconds to execute the list of commands in all "+str(numOfServers)+" servers.")
		return self.serversCmdDict
