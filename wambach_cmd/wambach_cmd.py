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
import paramiko, base64

from ssh_talker import talker as tlkr

command_dict = {}



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def dummy_funct(t):
   """
   """
   print 'dummy function' 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def watch_init(t):
   """
      Initial thought, watch file on probe,
      update probe files needed during boot process
   """
   pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_slice_ver(t,sl):
   """
   """
   cmd_ver = '/opt/qt600/bin/s%s 100f0' % sl
   cmd_date = '/opt/qt600/bin/s%s 100f4' % sl
   cmd_time = '/opt/qt600/bin/s%s 100f8' % sl
   st_in,st_out,st_err = t.snd_cmd(t.client,cmd_ver)
   l = st_out.readlines()
   #print l
   prn_result(l)
   st_in,st_out,sterr = t.snd_cmd(t.client,cmd_date)
   l = st_out.readlines()
   #print l
   prn_result(l)
   st_in,st_out,sterr = t.snd_cmd(t.client,cmd_time)
   l = st_out.readlines()
   #print l
   prn_result(l)

def get_s1_ver(t):
   """
   """
   get_slice_ver(t,1)

def get_s2_ver(t):
   """
   """
   get_slice_ver(t,2)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def reload_fpga(t, fpga=1, code='glan'):
   """
   """
   cmd_dbug_on = '/opt/qt600/bin/qteth%d enable debug' % fpga
   cmd_dbug_off = '/opt/qt600/bin/qteth%d disable debug' % fpga
   cmd_chg_fpga = '/opt/qt600/etc/init.d/change10gFPGA.bash %d %s' % (fpga,code)

   st_stuff = t.snd_cmd(t.client, cmd_dbug_on)
   st_stuff = t.snd_cmd(t.client, cmd_chg_fpga)
   prn_result(st_stuff[1].readlines())
   time.sleep(10)
   st_stuff = t.snd_cmd(t.client, cmd_dbug_off)

def reload_glan1(t):
   """
   """
   reload_fpga(t, 1,'glan')

def reload_glan2(t):
   """
   """
   reload_fpga(t, 2,'glan')

def reload_gpm1(t):
   """
   """
   reload_fpga(t, 1,'gpm')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def opt_parse():
   """
      parse the command line
      return options and arguments
   """
   parser = optparse.OptionParser(usage = usage())
   parser.add_option('-u', '--user', action='store',dest='user', default='.', help='user name')
   parser.add_option('-p', '--passwrd', action='store',dest='passwrd', default='.', help='pass word')
   # parser.add_option('-d', action='store',dest='dirt', default='.', help='head of directory tree')
   # parser.add_option('-x', action='store',dest='exclude', default=None, help='directorys to exclude')
   # parser.add_option('-A', action='store_true',dest='almost', default=False, help='Almost all files and directories')
   # parser.add_option('-v', action='store_true',dest='verbose', default=False, help='verbose')
   (options,args) = parser.parse_args()

   return (options, args)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def usage():
   """
   """
   u = 'usage: %prog cmd \n  where cmd is one of:\n'
   for k,(c,w) in command_dict.items():
      #print 'key: %s value is: %s' % (k,w)
      u += '\t%s - %s\n' % (k,w)
   return u

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
def exec_cmd(t,cmd):
   """
   """
   #print type(cmd)
   if isinstance(cmd,str):
      #print cmd
      stin,stout,sterr = t.snd_cmd(t.client,cmd)
      return (stin,stout,sterr)
   elif callable(cmd):
      #print 'this is a function'
      return cmd(t)

   return None



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#command_dict = {'reboot':('reboot','reboot probe')}
#command_dict['cyclePwr'] =('/opt/qt600/bin/fpga-load -s 1 -r 4d8 -v 1000','cycle Power')
command_dict['rescan'] = ('echo "1" > /sys/bus/pci/rescan','rescan the PCI bus')
command_dict['hw_init'] = ('/opt/qt600/etc/init.d/qt_hw_init start ','hw_init start')
command_dict['no_hw'] = ('mv /etc/qt_probe.conf /etc/qt_probe.conf.save','move "config" to save file')
command_dict['yes_hw'] = ('mv /etc/qt_probe.conf.save /etc/qt_probe.conf','restore "config" file')
command_dict['s1_ver'] = (get_s1_ver,'get slice 1 load version')
command_dict['s2_ver'] = (get_s2_ver,'get slice 2 load version')
command_dict['lspci'] = ('lspci -vt','lspci')
command_dict['lspci-s'] = ('lspci','short lspci')
command_dict['lspci-vd'] = ('lspci -vv -d 1172:0004','verbose lspci for device 1172:0004')
command_dict['cv1'] = ('/opt/qt600/bin/s1 100f0','get slice version')
command_dict['rglan1'] = (reload_glan1,'reload fpga1 with glan')
command_dict['rglan2'] = (reload_glan2,'reload fpga2 with glan')
command_dict['rgpm1'] = (reload_gpm1,'reload fpga1 with gpm')
command_dict['factory'] = ('cat /proc/factory', 'dump the factory file')
command_dict['appinfo'] = ('/opt/qt600/bin/appinfo', 'show appinfo')
command_dict['dummy'] = (dummy_funct,'')

if __name__ == "__main__":
   """
   """
   (option,arg) = opt_parse()
   t = tlkr('wambach', user='root', passwrd='celogic')

   if len(arg)  <= 0:
      print "not enough args"
      print "\t-h or --help"
      sys.exit(1)
   cmd = get_cmd(arg[0])
   if not cmd:
      print 'command "%s" not found' % (arg[0])
      sys.exit(1) 
   #print cmd
   st_stuff = exec_cmd(t,cmd)
   if st_stuff:
      if st_stuff[1]:
         #print 'is stdout'
         prn_result(st_stuff[1])
      if st_stuff[2]:
         #print 'is stderr'
         prn_result(st_stuff[2])
   t.close()
   sys.exit(0)

