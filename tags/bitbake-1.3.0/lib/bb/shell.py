#!/usr/bin/env python
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# Copyright (C) 2005 Michael 'Mickey' Lauer <mickey@Vanille.de>, Vanille Media
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA.
#

"""
BitBake Shell

General Question to be decided: Make it a full-fledged Python Shell or
retain the simple command line interface like it is at the moment?

TODO:
    * Fix bugs (see below)
    * decide whether to use a special mode for '-b' or leave it like it is
    * specify tasks
    * specify force
    * command to reparse just one (or more) bbfile(s)
    * automatic check if reparsing is necessary (inotify?)
    * bb file wizard

BUGS:
    * somehow the stamps or the make build cache gets confused.
      Reproduce this by calling rebuild on a bbfile twice.
      1st, some tasks are called twice (do_fetch for instance),
      2nd, no tasks are called anymore on the second rebuild.
      Obviously executeOneBB is corrupting some state variables
      or making some bogus assumptions about state and/or control flow
"""

try:
    set
except NameError:
    from sets import Set as set
import sys, os, imp, readline
imp.load_source( "bitbake", os.path.dirname( sys.argv[0] )+"/bitbake" )
from bb import make, data

__version__ = 0.2
__credits__ = """BitBake Shell Version %2.1f (C) 2005 Michael 'Mickey' Lauer <mickey@Vanille.de>
Type 'help' for more information, press CTRL-D to exit.""" % __version__

cmds = {}
leave_mainloop = False
cooker = None
parsed = False
debug = os.environ.get( "BBSHELL_DEBUG", "" ) != ""
history_file = "%s/.bbsh_history" % os.environ.get( "HOME" )

##########################################################################
# Commands
##########################################################################

def buildCommand( params, cmd = "build" ):
    """Build a .bb file or a provider"""
    try:
        name = params[0]
    except IndexError:
        print "Usage: build <bbfile|provider>"
    else:
        make.options.cmd = cmd
        cooker.build_cache = []
        cooker.build_cache_fail = []

        if name.endswith( ".bb" ):
            cooker.executeOneBB( completeFilePath( name ) )
        else:
            if not parsed:
                print "BBSHELL: D'oh! The .bb files haven't been parsed yet. Next time call 'parse' before building stuff. This time I'll do it for 'ya."
                parseCommand( None )
            cooker.buildPackage( name )

def cleanCommand( params ):
    """Clean a .bb file or a provider"""
    buildCommand( params, "clean" )

def editCommand( params ):
    """Call $EDITOR on a .bb file"""
    try:
        name = params[0]
    except IndexError:
        print "Usage: edit <bbfile>"
    else:
        os.system( "%s %s" % ( os.environ.get( "EDITOR" ), completeFilePath( name ) ) )

def environmentCommand( params ):
    """Dump out the outer BitBake environment (see bbread)"""
    data.emit_env(sys.__stdout__, make.cfg, True)

def execCommand( params ):
    """Execute one line of python code"""
    exec " ".join( params ) in locals(), globals()

def exitShell( params ):
    """Leave the BitBake Shell"""
    if debug: print "(setting leave_mainloop to true)"
    global leave_mainloop
    leave_mainloop = True

def parseCommand( params ):
    """(Re-)parse .bb files and calculate the dependency graph"""
    cooker.status = cooker.ParsingStatus()
    ignore = data.getVar("ASSUME_PROVIDED", make.cfg, 1) or ""
    cooker.status.ignored_dependencies = set( ignore.split() )
    cooker.handleCollections( data.getVar("BBFILE_COLLECTIONS", make.cfg, 1) )

    make.collect_bbfiles( cooker.myProgressCallback )
    cooker.buildDepgraph()
    global parsed
    parsed = True
    print

def printCommand( params ):
    """Print the contents of an outer BitBake environment variable"""
    try:
        var = params[0]
    except IndexError:
        print "Usage: print <variable>"
    else:
        value = data.getVar( var, make.cfg, 1 )
        print value

def pythonCommand( params ):
    """Enter the expert mode - an interactive BitBake Python Interpreter"""
    sys.ps1 = "EXPERT BB>>> "
    sys.ps2 = "EXPERT BB... "
    import code
    python = code.InteractiveConsole( dict( globals() ) )
    python.interact( "BBSHELL: Expert Mode - BitBake Python %s\nType 'help' for more information, press CTRL-D to switch back to BBSHELL." % sys.version )

def setVarCommand( params ):
    """Set an outer BitBake environment variable"""
    try:
        var, value = params
    except ValueError, IndexError:
        print "Usage: set <variable> <value>"
    else:
        data.setVar( var, value, make.cfg )
        print "OK"

def rebuildCommand( params ):
    """Clean and rebuild a .bb file or a provider"""
    buildCommand( params, "clean" )
    buildCommand( params, "build" )

def testCommand( params ):
    """Just for testing..."""
    print "testCommand called with '%s'" % params

def whichCommand( params ):
    """Computes the preferred and latest provider for a given dependency"""
    try:
        var = params[0]
    except IndexError:
        print "Usage: which <provider>"
    else:
        print "Sorry, not yet implemented"

##########################################################################
# Common helper functions
##########################################################################

def completeFilePath( bbfile ):
    if not make.pkgdata: return bbfile
    for key in make.pkgdata.keys():
        if key.endswith( bbfile ):
            return key
    return bbfile

##########################################################################
# Startup / Shutdown
##########################################################################
def init():
    """Register commands and set up readline"""
    registerCommand( "help", showHelp )
    registerCommand( "exit", exitShell )

    registerCommand( "build", buildCommand )
    registerCommand( "clean", cleanCommand )
    registerCommand( "edit", editCommand )
    registerCommand( "environment", environmentCommand )
    registerCommand( "exec", execCommand )
    registerCommand( "parse", parseCommand )
    registerCommand( "print", printCommand )
    registerCommand( "python", pythonCommand )
    registerCommand( "rebuild", rebuildCommand )
    registerCommand( "set", setVarCommand )
    registerCommand( "test", testCommand )

    readline.set_completer( completer )
    readline.set_completer_delims( " " )
    readline.parse_and_bind("tab: complete")

    try:
        global history_file
        readline.read_history_file( history_file )
    except IOError:
        pass  # It doesn't exist yet.

def cleanup():
    if debug: print "(writing command history)"
    try:
        global history_file
        readline.write_history_file( history_file )
    except:
        print "BBSHELL: Unable to save command history"

def completer( text, state ):
    if debug: print "(completer called with text='%s', state='%d'" % ( text, state )

    if state == 0:
        line = readline.get_line_buffer()
        if " " in line:
            line = line.split()
            # we are in second (or more) argument
            if line[0] == "print" or line[0] == "set":
                allmatches = make.cfg.keys()
            else:
                if make.pkgdata is None: allmatches = [ "(No Matches Available. Parsed yet?)" ]
                else: allmatches = [ x.split("/")[-1] for x in make.pkgdata.keys() ]
        else:
            # we are in first argument
            allmatches = cmds.iterkeys()

        completer.matches = [ x for x in allmatches if x[:len(text)] == text ]
        #print "completer.matches = '%s'" % completer.matches
    if len( completer.matches ) > state:
        return completer.matches[state]
    else:
        return None

def showCredits():
    print __credits__

def showHelp( *args ):
    """Show a comprehensive list of commands and their purpose"""
    print "="*35, "Available Commands", "="*35
    for cmd, func in cmds.items():
        print "| %s | %s" % (cmd.ljust(max([len(x) for x in cmds.keys()])), func.__doc__)
    print "="*88

def registerCommand( command, function ):
    cmds[command] = function

def processCommand( command, params ):
    if debug: print "(processing command '%s'...)" % command
    if command in cmds:
        result = cmds[command]( params )
    else:
        print "Error: '%s' command is not a valid command." % command
        return
    if debug: print "(result was '%s')" % result

def main():
    while not leave_mainloop:
        try:
            cmdline = raw_input( "BB>> " )
            if cmdline:
                if ' ' in cmdline:
                    processCommand( cmdline.split()[0], cmdline.split()[1:] )
                else:
                    processCommand( cmdline, "" )
        except EOFError:
            print
            return
        except KeyboardInterrupt:
            print

def start( aCooker ):
    global cooker
    cooker = aCooker
    showCredits()
    init()
    main()
    cleanup()

if __name__ == "__main__":
    print "BBSHELL: Sorry, this program should only be called by BitBake."
