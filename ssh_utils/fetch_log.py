#!/usr/bin/env python

"""
   A quick demo on using the talker class from ssh_talker.py
   with sftp.

   Remember, there must be a __init__.py file in the directory
   where ssh_talker.py is located to use only the talker class
"""

import sys
import time
import optparse
#import paramiko, base64

from ssh_talker import talker

command_dict = {}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def opt_parse():
   """
      parse the command line
      return options and arguments
   """
   parser = optparse.OptionParser(usage = usage())
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



if __name__ == '__main__':
   """
   """
   (option,arg) = opt_parse()
   t = talker('wambach', user='root',passwrd='celogic')


   remote_file = '/var/log/messages'
   local_file = '/tmp/msgs'

   t.get(remote_file, local_file)

   for f in t.sftp_list('/tmp/cap'):
      print f

   t.close()




