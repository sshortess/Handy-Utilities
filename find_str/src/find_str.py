#!/usr/bin/env python

"""
   Search the current directory tree for a string in files, skip hidden files (.file)
   and hidden directories (.directory)
   Todo:
      add parsing of command line for options
      add -A to include hidden files and directories
      add -l to follow links (be careful about directory recursion)
      add -v to report broken links and other non-existant files

"""

import os, sys
from os.path import join
import re
import optparse

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def arg_parse():
   """
      parse the command line
      return options and arguments
   """
   parser = optparse.OptionParser()
   # parser.add_option('-d', action='store',dest='dirt', default='.', help='head of directory tree')
   parser.add_option('-x', action='store',dest='exclude', default=None, help='directories to exclude')
   parser.add_option('-i', action='store_true',dest='nocase', default=False, help='ignore case')
   # parser.add_option('-A', action='store_true',dest='almost', default=False, help='Almost all files and directories')
   # parser.add_option('-l', action='store_true',dest='links', default=False, help='follow links')
   # parser.add_option('-v', action='store_true',dest='verbose', default=False, help='verbose')
   (options,args) = parser.parse_args()

   return (options, args)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def xcld_dir(dirLst,exclude=None):
   """
      remove directories to exclude
   """
   if not exclude:
      return dirLst
   xdirs = exclude.split(',')
   # print xdirs
   for xdir in xdirs:
      try:
         ndx = dirLst.index(xdir)
         del dirLst[ndx]
      except ValueError:
         pass

   return dirLst      

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def find_str(fnd_str, dirt='.',opt=None):
   """
      for all files in directory tree
         read file
         look for string
         if found
            report
   """
   flg = 0  #initialize search flag
   if opt.nocase:
      flg |= re.IGNORECASE
   # compile regular expression (re)
   p = re.compile(fnd_str,flags=flg)

   for root,dirs,files in os.walk(dirt, topdown=True, followlinks=False):
      # don't look in hidden directories 
      dirs[:] = [d for d in dirs if not d.startswith('.')]  # remove the dot(.) directories
      #if opt.exclude:
      dirs = xcld_dir(dirs,opt.exclude)
      for name in files:
         if name.startswith('.'):      # skip files that start with dot(.), hidden
            continue
         # this works, but is slow
         # os.system('grep -l http_prox=10 "%s"' % join(root,name) )
         # a better/faster (?) way??
         # open file, then use re.search()
         try:
            for line in open(join(root,name),'r'):
               # print line
               #if re.search(fnd_str,line,flags=flg) != None:
               if p.search(line) != None:
                  print join(root,name)
                  break
         except IOError:
            if not os.path.exists(join(root,name)):
               # print "IOError: Broken Link %s" % join(root,name)   #report broken links separate
               pass
            else:
               print "IOError: No file or directory %s" % join(root,name)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
   (options,args) = arg_parse()
   if len(args) >= 1:
      print 'Looking for:', args[0]
      if options.exclude:
         print '\texcluding directories', options.exclude
      try:
         find_str(args[0],opt=options)
      except (KeyboardInterrupt):      #don't do anything, just quit
         pass
      except:  #warn user of an oops
         raise

   print #blank line when done
   
