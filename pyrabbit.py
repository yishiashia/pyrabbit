#!/usr/bin/env python
#coding=utf8

import os, sys, time
from rabbit_thread import rabbitThread

def createDaemon():
  ## fork child process and exit current process
  try:
    pid = os.fork()
    if pid > 0:sys.exit(0)
  except OSError,error:
    print 'fork'
    sys.exit(1)

  ## change current working folder of child process
  os.chdir("/")
  ## create new session, make child process be the group leader of new session
  os.setsid()
  ## update umask of working folder
  os.umask(0)

  ## create grandson process and exit child process
  try:
    pid = os.fork()
    if pid > 0:
      print "Daemon PID %d"%pid
      sys.exit(0)
  except OSError,error:
    print "fork"
    sys.exit(1)
  run()

def run():
  thread_number = 5

  t = []
  for i in range(thread_number):
    t.append(rabbitThread())
    t[i].start()

  while True:
    time.sleep(120)
    for i in range(thread_number):
      t[i].terminate()
      t[i] = rabbitThread()
      t[i].start()

if __name__=='__main__':
  createDaemon()
