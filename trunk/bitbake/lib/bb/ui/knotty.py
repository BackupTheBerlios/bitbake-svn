#
# BitBake (No)TTY UI Implementation
#
# Handling output to TTYs or files (no TTY)
#
# Copyright (C) 2006-2007 Richard Purdie
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os

import sys
import itertools
import xmlrpclib

parsespin = itertools.cycle( r'|/-\\' )

def init(server, eventHandler):

    # Get values of variables which control our output
    includelogs = server.runCommand(["getVariable", "BBINCLUDELOGS"])
    loglines = server.runCommand(["getVariable", "BBINCLUDELOGS_LINES"])

    try:
        cmdline = server.runCommand(["getCmdLineAction"])
        #print cmdline
        if not cmdline:
            return 1
        ret = server.runCommand(cmdline)
        if ret != True:
            print "Couldn't get default commandline! %s" % ret
            return 1
    except xmlrpclib.Fault, x:
        print "XMLRPC Fault getting commandline:\n %s" % x
        return 1

    shutdown = 0
    return_value = 0
    while True:
        try:
            event = eventHandler.waitEvent(0.25)
            if event is None:
                continue
            #print event
            if event[0].startswith('bb.msg.MsgPlain'):
                print event[1]['_message']
                continue
            if event[0].startswith('bb.msg.MsgDebug'):
                print 'DEBUG: ' + event[1]['_message']
                continue
            if event[0].startswith('bb.msg.MsgNote'):
                print 'NOTE: ' + event[1]['_message']
                continue
            if event[0].startswith('bb.msg.MsgWarn'):
                print 'WARNING: ' + event[1]['_message']
                continue
            if event[0].startswith('bb.msg.MsgError'):
                return_value = 1
                print 'ERROR: ' + event[1]['_message']
                continue
            if event[0].startswith('bb.msg.MsgFatal'):
                return_value = 1
                print 'FATAL: ' + event[1]['_message']
                break
            if event[0].startswith('bb.build.TaskFailed'):
                return_value = 1
                logfile = event[1]['logfile']
                if logfile:
                    print "ERROR: Logfile of failure stored in %s." % logfile
                    if 1 or includelogs:
                        print "Log data follows:"
                        f = open(logfile, "r")
                        lines = []
                        while True:
                            l = f.readline()
                            if l == '':
                                break
                            l = l.rstrip()
                            if loglines:
                                lines.append(' | %s' % l)
                                if len(lines) > int(loglines):
                                    lines.pop(0)
                            else:
                                print '| %s' % l
                        f.close()
                        if lines:
                            for line in lines:
                                print line
            if event[0].startswith('bb.build.Task'):
                print "NOTE: %s" % event[1]['_message']
                continue
            if event[0].startswith('bb.event.ParseProgress'):
                x = event[1]['sofar']
                y = event[1]['total']
                if os.isatty(sys.stdout.fileno()):
                    sys.stdout.write("\rNOTE: Handling BitBake files: %s (%04d/%04d) [%2d %%]" % ( parsespin.next(), x, y, x*100/y ) )
                    sys.stdout.flush()
                else:
                    if x == 1:
                        sys.stdout.write("Parsing .bb files, please wait...")
                        sys.stdout.flush()
                    if x == y:
                        sys.stdout.write("done.")
                        sys.stdout.flush()
                if x == y:
                    print("\nParsing finished. %d cached, %d parsed, %d skipped, %d masked, %d errors." 
                        % ( event[1]['cached'], event[1]['parsed'], event[1]['skipped'], event[1]['masked'], event[1]['errors']))
                continue

            if event[0] == 'bb.command.CookerCommandCompleted':
                break
            if event[0] == 'bb.command.CookerCommandFailed':
                return_value = 1
                print "Command execution failed: %s" % event[1]['error']
                break
            if event[0] == 'bb.cooker.CookerExit':
                break

            # ignore
            if event[0].startswith('bb.event.BuildStarted'):
                continue
            if event[0].startswith('bb.event.BuildCompleted'):
                continue
            if event[0].startswith('bb.event.MultipleProviders'):
                continue
            if event[0].startswith('bb.runqueue.runQueue'):
                continue
            if event[0].startswith('bb.event.StampUpdate'):
                continue
            if event[0].startswith('bb.event.ConfigParsed'):
                continue
            print "Unknown Event: %s" % event

        except KeyboardInterrupt:
            if shutdown == 2:
                print "\nThird Keyboard Interrupt, exit.\n"
                break
            if shutdown == 1:
                print "\nSecond Keyboard Interrupt, stopping...\n"
                server.runCommand(["stateStop"])
            if shutdown == 0:
                print "\nKeyboard Interrupt, closing down...\n"
                server.runCommand(["stateShutdown"])
            shutdown = shutdown + 1
            pass
    return return_value
