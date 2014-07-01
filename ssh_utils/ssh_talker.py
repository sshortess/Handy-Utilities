#!/usr/bin/env python

"""
I primarialy kept this file, not for the host command part, but for
the expample of how to use paramiko, the python ssh library.

It's also a handy reminder how to use a dictionary to look up and execute
commands, and how to limit the size of the output line to fit the terminal
window.
"""

import fcntl, struct
import sys
import time
import optparse
import getpass
import paramiko, base64


class talker:

   def __init__(self, host, port=22, user='anonymouw', passwrd='none'):
      """
      """
      self.dict_cmd = {}
      self.host = host
      self.user = user
      self.passwrd = passwrd
      self.port = port
      self.client = self.mk_myclient()
      self.sftp_transport = ''

   
   def mk_myclient(self):
      """
      """
      self.client = self.mk_client();
      return self.client
      
   def mk_client(self):
      """
      """
      client = paramiko.SSHClient()
      client.load_system_host_keys()
      client.set_missing_host_key_policy(paramiko.WarningPolicy())
      return client

   def set_cmd_dict(cmd_dict):
      """
         just in case you want to pass the command dictionary with object
      """
      self.dict_cmd = cmd_dict
      return self.dict_cmd

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def mk_my_sftp_transport(self):
      """
      """
      self.sftp_transport = mk_sftp_transport()
      return self.sftp_transport

   def mk_sftp_transport(self):
      """
      """
      sftp_trans = paramiko.Transport((self.host,self.port))
      return sftp_trans
   
   def mk_sftp_channel(self):
      """
      """
      transport = paramiko.Transport((self.host, self.port))
      transport.connect(username = self.user, password = self.passwrd)
      sftp = paramiko.SFTPClient.from_transport(transport)
      return sftp

   def get(self,remote_file,local_file):
      """
      """
      sftp = self.mk_sftp_channel()
      sftp.get(remote_file, local_file)
      sftp.close()

   def get_all(self,remotepath,localpath):
      """
      #  recursively download a full directory
      #  Harder than it sounded at first, since paramiko won't walk
      #
      # For the record, something like this would gennerally be faster:
      # ssh user@host 'tar -cz /source/folder' | tar -xz
      """
      print "Silly rabit, use \"ssh -n user@host 'tar cz remote_path' | tar xz\" ...!!"


   def put(self, local_path, remote_path):
      """
      """
      sftp = self.mk_sftp_channel()
      sftp.put(local_path, remote_path)
      sftp.close()

   def put_all(self,localpath,remotepath):
      """
      #  recursively upload a full directory
      """
      sftp = self.mk_sftp_channel()
      os.chdir(os.path.split(localpath)[0])
      parent=os.path.split(localpath)[1]
      for walker in os.walk(parent):
         try:
            self.sftp.mkdir(os.path.join(remotepath,walker[0]))
         except:
            pass
         for file in walker[2]:
            self.put(os.path.join(walker[0],file),os.path.join(remotepath,walker[0],file))
      sftp.close()

   def sftp_list(self, remote_path):
      """
      """
      sftp = self.mk_sftp_channel()
      file_list = sftp.listdir(remote_path)
      sftp.close()
      return file_list

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def conn_shell(self, client):
      """
      """
      try:
         client.connect(self.host,self.port,self.user,self.passwrd)
         chan = client.invoke_shell()
         return chan
      except paramiko.ChannelException:
         print 'ChannelException: could not open channel'
         return None

   def snd_cmd(self,client, cmd):
      """
      """
      #print cmd
      try:
         client.connect(self.host,self.port,self.user,self.passwrd)
         (st_in, st_out, st_err) = client.exec_command(cmd)
         return (st_in, st_out, st_err)
      except paramiko.ChannelException:
         print 'ChannelException: could not open channel'
         return None

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def close(self):
      """
      """
      self.client.close()

   def client_close(self, client):
      """
      """
      client.close()

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def get_cmd(self,ucmd):
      """
      """
      try:
         cmd = self.dict_cmd[ucmd]
         return cmd
      except KeyError:
         # print 'command not found'
         return None

   def exec_cmd(self,cmd):
      """
      """
      #print type(cmd)
      if isinstance(cmd,str):
         #print cmd
         stin,stout,sterr = self.snd_cmd(self.client,cmd)
         return (stin,stout,sterr)
      elif callable(cmd):
         #print 'this is a function'
         return cmd()
      return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def opt_parse():
   """
      parse the command line
      return options and arguments
   """
   parser = optparse.OptionParser(usage = usage())
   parser.add_option('--user', action='store',dest='username', default=None, help='username on remote host')
   parser.add_option('--password', action='store',dest='passwrd', default=None, help='remote host password')
   parser.add_option('--port', action='store',dest='port', default=22, help='remote port')
   # parser.add_option('-d', action='store',dest='dirt', default='.', help='head of directory tree')
   # parser.add_option('-x', action='store',dest='exclude', default=None, help='directorys to exclude')
   # parser.add_option('-A', action='store_true',dest='almost', default=False, help='Almost all files and directories')
   # parser.add_option('-v', action='store_true',dest='verbose', default=False, help='verbose')
   (options,args) = parser.parse_args()

   return (args, options)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def usage():
   """
   """
   u = 'usage: %prog cmd \n  where cmd is one of:\n'
   for k,(c,w) in command_dict.items():
      #print 'key: %s value is: %s' % (k,w)
      u += '\t%s - %s\n' % (k,w)
   return u

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def process_args(arg, options):
   """
   """
   if len(arg)  <= 0:
      print "not enough args"
      print "\t-h or --help"
      sys.exit(1)

   hostname = None
   cmd = get_cmd(arg[0])
   if not cmd:
      #hopefully, if not a command, the arg is a host name
      if len(arg) >1:
         hostname = arg.pop(0)
         cmd = get_cmd(arg[0])
         if not cmd:
            print 'command "%s" not found' % (arg[0])
      else:
         print 'command "%s" not found' % (arg[0])
         
   if cmd:
      arg.pop(0)
   
   return (hostname, cmd, arg, options)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_user_pass(arg,option):
   """
   """
   if not option.username:
      username = getpass.getuser()
   else:
      username = option.username

   if not option.passwrd: 
      passwrd = getpass.getpass()
   else:
      passwrd = option.passwrd

   return (username, passwrd)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_term_size():
   """
      quick and dirty 
   """
   from  getTermSize import getTerminalSize
   try:
      cr = getTerminalSize()
      return cr
   except:
      return None
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def prn_result(res, trim=True):
   """
   """
   if trim:
      prn_result_trim(res)
   else:
      prn_result_notrim(res)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def prn_result_trim(res):
   """
   """
   for line in res:
      pl = line.strip('\n').expandtabs(4)
      cr = get_term_size()
      if cr:
         if len(pl) <= cr[0]:
            print pl
         else:
            print pl[:cr[0]]
      else:
         prn_result(res, False)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def prn_result_notrim(res):
   """
   """
   for line in res:
      print line.strip('\n')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_cmd(ucmd):
   """
   """
   try:
      cmd,w = command_dict[ucmd]
      return cmd
   except KeyError:
      # print 'command not found'
      return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def exec_cmd(t,cmd,stuff=None):
   """
   """
   #print type(cmd)
   if isinstance(cmd,str):
      #print cmd
      stin,stout,sterr = t.snd_cmd(t.client,cmd)
      return (stin,stout,sterr)
   elif callable(cmd):
      #print 'this is a function'
      return cmd(t,stuff)

   return None


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def dummy_funct(t,stuff=None):
   """
   """
   print 'dummy function' 


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_ls(t,stuff=None):
   """
      get remote directory list
   """
   if not stuff:
      return None

   arg, option = stuff
   remote_dir = arg[0]
   lst = t.sftp_list(remote_dir)
   prn_result(lst,False)
   return lst


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_file(t,remote_path, local_path):
   """
      get file from remote
   """

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def put_file(t,local_path, remote_path):
   """
      put file on remote
   """

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
command_dict = {}
command_dict['rescan'] = ('echo "1" > /sys/bus/pci/rescan','rescan the PCI bus')
command_dict['lspci'] = ('lspci -vt','lspci verbose tree')
command_dict['lspci-s'] = ('lspci','short lspci')
command_dict['get_ls'] = (get_ls,'get remote directory file list')
command_dict['get_file'] = (get_ls,'get remote file from host')
command_dict['get_ls'] = (get_ls,'put file to remote host')
command_dict['dummy'] = (dummy_funct,'demostration of how to write a function')

if __name__ == "__main__":
   """
   """
   # get arguments and options
   (arg, option) = opt_parse()

   (hostname,cmd,arg,option) = process_args(arg,option)
   # get host name (if not in arg list) 
   if not hostname:
      hostname = raw_input('remote host: ')

   username, passwrd = get_user_pass(arg, option)

   t = talker(hostname, option.port, user=username, passwrd=passwrd)
   #(si,so,se) = t.exec_cmd(cmd)
   st_stuff = exec_cmd(t,cmd,(arg,option))
   if st_stuff:
      if st_stuff[1]:
         #print 'is stdout'
         prn_result(st_stuff[1])
      if st_stuff[2]:
         #print 'is stderr'
         prn_result(st_stuff[2])
   t.close()
   sys.exit(0)

