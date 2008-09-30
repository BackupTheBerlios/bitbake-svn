#!/usr/bin/env python
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# Copyright (C) 2003, 2004  Chris Larson
# Copyright (C) 2003, 2004  Phil Blundell
# Copyright (C) 2003 - 2005 Michael 'Mickey' Lauer
# Copyright (C) 2005        Holger Hans Peter Freyther
# Copyright (C) 2005        ROAD GmbH
# Copyright (C) 2006 - 2007 Richard Purdie
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

import sys, os, getopt, glob, copy, os.path, re, time
import bb
from bb import utils, data, parse, event, cache, providers, taskdata, runqueue
from bb import xmlrpcserver, command
from sets import Set
import itertools, sre_constants

class MultipleMatches(Exception):
    """
    Exception raised when multiple file matches are found
    """

class ParsingErrorsFound(Exception):
    """
    Exception raised when parsing errors are found
    """

class NothingToBuild(Exception):
    """
    Exception raised when there is nothing to build
    """


# Different states cooker can be in
cookerClean = 1
cookerParsed = 2

# Different action states the cooker can be in
cookerRun = 1           # Cooker is running normally
cookerShutdown = 2      # Active tasks should be brought to a controlled stop
cookerStop = 3          # Stop, now!

#============================================================================#
# BBCooker
#============================================================================#
class BBCooker:
    """
    Manages one bitbake build run
    """

    def __init__(self, configuration):
        self.status = None

        self.cache = None
        self.bb_cache = None

        self.server = bb.xmlrpcserver.BitBakeXMLRPCServer(self)
        #self.server.register_function(self.showEnvironment)

        self.configuration = configuration

        if self.configuration.verbose:
            bb.msg.set_verbose(True)

        if self.configuration.debug:
            bb.msg.set_debug_level(self.configuration.debug)
        else:
            bb.msg.set_debug_level(0)

        if self.configuration.debug_domains:
            bb.msg.set_debug_domains(self.configuration.debug_domains)

        self.configuration.data = bb.data.init()

        for f in self.configuration.file:
            self.parseConfigurationFile( f )

        self.parseConfigurationFile( os.path.join( "conf", "bitbake.conf" ) )

        if not self.configuration.cmd:
            self.configuration.cmd = bb.data.getVar("BB_DEFAULT_TASK", self.configuration.data, True) or "build"

        bbpkgs = bb.data.getVar('BBPKGS', self.configuration.data, True)
        if bbpkgs:
            self.configuration.pkgs_to_build.extend(bbpkgs.split())

        #
        # Special updated configuration we use for firing events
        #
        self.configuration.event_data = bb.data.createCopy(self.configuration.data)
        bb.data.update_data(self.configuration.event_data)

        # TOSTOP must not be set or our children will hang when they output
        fd = sys.stdout.fileno()
        if os.isatty(fd):
            import termios
            tcattr = termios.tcgetattr(fd)
            if tcattr[3] & termios.TOSTOP:
                bb.msg.note(1, bb.msg.domain.Build, "The terminal had the TOSTOP bit set, clearing...")
                tcattr[3] = tcattr[3] & ~termios.TOSTOP
                termios.tcsetattr(fd, termios.TCSANOW, tcattr)

        # Change nice level if we're asked to
        nice = bb.data.getVar("BB_NICE_LEVEL", self.configuration.data, True)
        if nice:
            curnice = os.nice(0)
            nice = int(nice) - curnice
            bb.msg.note(2, bb.msg.domain.Build, "Renice to %s " % os.nice(nice))
 
        # Parse any commandline into actions
        if self.configuration.show_environment:
            self.commandlineAction = None

            if 'world' in self.configuration.pkgs_to_build:
                bb.error("'world' is not a valid target for --environment.")
            elif len(self.configuration.pkgs_to_build) > 1:
                bb.error("Only one target can be used with the --environment option.")
            elif self.configuration.buildfile and len(self.configuration.pkgs_to_build) > 0:
                bb.error("No target should be used with the --environment and --buildfile options.")
            else:
                self.commandlineAction = ["showEnvironment", self.configuration.buildfile, self.configuration.pkgs_to_build]
        elif self.configuration.buildfile is not None:
            self.commandlineAction = ["buildFile", self.configuration.buildfile, self.configuration.cmd]
        elif self.configuration.show_versions:
            self.commandlineAction = ["showVersions"]
        elif self.configuration.parse_only:
            self.commandlineAction = ["parseFiles"]
        elif self.configuration.dot_graph:
            if self.configuration.pkgs_to_build:
                self.commandlineAction = ["generateDotGraph", self.configuration.pkgs_to_build]
            else:
                self.commandlineAction = None
                bb.error("Please specify a package name for dependency graph generation.")
        else:
            if self.configuration.pkgs_to_build:
                self.commandlineAction = ["buildTargets", self.configuration.pkgs_to_build]
            else:
                self.commandlineAction = None
                bb.error("Nothing to do.  Use 'bitbake world' to build everything, or run 'bitbake --help' for usage information.")

        # FIXME - implement
        #if self.configuration.interactive:
        #    self.interactiveMode()

        self.command = bb.command.Command(self)
        self.cookerIdle = True
        self.cookerState = cookerClean
        self.cookerAction = cookerRun
        self.server.register_idle_function(self.runCommands, self)


    def runCommands(self, server, data, abort):
        """
        Run any queued offline command
        This is done by the idle handler so it runs in true context rather than
        tied to any UI.
        """
        if self.cookerIdle and not abort:
            self.command.runOfflineCommand()

        # Always reschedule
        return True

    def tryBuildPackage(self, fn, item, task, the_data):
        """
        Build one task of a package, optionally build following task depends
        """
        bb.event.fire(bb.event.PkgStarted(item, the_data))
        try:
            if not self.configuration.dry_run:
                bb.build.exec_task('do_%s' % task, the_data)
            bb.event.fire(bb.event.PkgSucceeded(item, the_data))
            return True
        except bb.build.FuncFailed:
            bb.msg.error(bb.msg.domain.Build, "task stack execution failed")
            bb.event.fire(bb.event.PkgFailed(item, the_data))
            raise
        except bb.build.EventException, e:
            event = e.args[1]
            bb.msg.error(bb.msg.domain.Build, "%s event exception, aborting" % bb.event.getName(event))
            bb.event.fire(bb.event.PkgFailed(item, the_data))
            raise

    def tryBuild(self, fn):
        """
        Build a provider and its dependencies. 
        build_depends is a list of previous build dependencies (not runtime)
        If build_depends is empty, we're dealing with a runtime depends
        """

        the_data = self.bb_cache.loadDataFull(fn, self.configuration.data)

        item = self.status.pkg_fn[fn]

        #if bb.build.stamp_is_current('do_%s' % self.configuration.cmd, the_data):
        #    return True

        return self.tryBuildPackage(fn, item, self.configuration.cmd, the_data)

    def showVersions(self):

        # Need files parsed
        self.updateCache()

        pkg_pn = self.status.pkg_pn
        preferred_versions = {}
        latest_versions = {}

        # Sort by priority
        for pn in pkg_pn.keys():
            (last_ver,last_file,pref_ver,pref_file) = bb.providers.findBestProvider(pn, self.configuration.data, self.status)
            preferred_versions[pn] = (pref_ver, pref_file)
            latest_versions[pn] = (last_ver, last_file)

        pkg_list = pkg_pn.keys()
        pkg_list.sort()

        bb.msg.plain("%-35s %25s %25s" % ("Package Name", "Latest Version", "Preferred Version"))
        bb.msg.plain("%-35s %25s %25s\n" % ("============", "==============", "================="))

        for p in pkg_list:
            pref = preferred_versions[p]
            latest = latest_versions[p]

            prefstr = pref[0][0] + ":" + pref[0][1] + '-' + pref[0][2]
            lateststr = latest[0][0] + ":" + latest[0][1] + "-" + latest[0][2]

            if pref == latest:
                prefstr = ""

            bb.msg.plain("%-35s %25s %25s" % (p, lateststr, prefstr))

    def showEnvironment(self, buildfile = None, pkgs_to_build = []):
        """
        Show the outer or per-package environment
        """
        fn = None
        envdata = None

        if buildfile:
            self.cb = None
            self.bb_cache = bb.cache.init(self)
            fn = self.matchFile(buildfile)
        elif len(pkgs_to_build) == 1:
            self.updateCache()

            localdata = data.createCopy(self.configuration.data)
            bb.data.update_data(localdata)
            bb.data.expandKeys(localdata)

            taskdata = bb.taskdata.TaskData(self.configuration.abort)
            taskdata.add_provider(localdata, self.status, pkgs_to_build[0])
            taskdata.add_unresolved(localdata, self.status)

            targetid = taskdata.getbuild_id(pkgs_to_build[0])
            fnid = taskdata.build_targets[targetid][0]
            fn = taskdata.fn_index[fnid]
        else:
            envdata = self.configuration.data

        if fn:
            try:
                envdata = self.bb_cache.loadDataFull(fn, self.configuration.data)
            except IOError, e:
                bb.msg.error(bb.msg.domain.Parsing, "Unable to read %s: %s" % (fn, e))
                raise
            except Exception, e:
                bb.msg.error(bb.msg.domain.Parsing, "%s" % e)
                raise

        class dummywrite:
            def __init__(self):
                self.writebuf = ""
            def write(self, output):
                self.writebuf = self.writebuf + output

        # emit variables and shell functions
        try:
            data.update_data(envdata)
            wb = dummywrite()
            data.emit_env(wb, envdata, True)
            bb.msg.plain(wb.writebuf)
        except Exception, e:
            bb.msg.fatal(bb.msg.domain.Parsing, "%s" % e)
        # emit the metadata which isnt valid shell
        data.expandKeys(envdata)
        for e in envdata.keys():
            if data.getVarFlag( e, 'python', envdata ):
                bb.msg.plain("\npython %s () {\n%s}\n" % (e, data.getVar(e, envdata, 1)))

    def generateDepTreeData(self, pkgs_to_build):
        """
        Create a dependency tree of pkgs_to_build, returning the data.
        """

        # Need files parsed
        self.updateCache()

        pkgs_to_build = self.checkPackages(pkgs_to_build)

        localdata = data.createCopy(self.configuration.data)
        bb.data.update_data(localdata)
        bb.data.expandKeys(localdata)
        taskdata = bb.taskdata.TaskData(self.configuration.abort)

        runlist = []
        for k in pkgs_to_build:
            taskdata.add_provider(localdata, self.status, k)
            runlist.append([k, "do_%s" % self.configuration.cmd])
        taskdata.add_unresolved(localdata, self.status)

        rq = bb.runqueue.RunQueue(self, self.configuration.data, self.status, taskdata, runlist)
        rq.prepare_runqueue()

        seen_fnids = []  
        depend_tree = {}
        depend_tree["depends"] = {}
        depend_tree["tdepends"] = {}
        depend_tree["pn"] = {}
        depend_tree["rdepends-pn"] = {}
        depend_tree["packages"] = {}
        depend_tree["rdepends-pkg"] = {}
        depend_tree["rrecs-pkg"] = {}

        for task in range(len(rq.runq_fnid)):
            taskname = rq.runq_task[task]
            fnid = rq.runq_fnid[task]
            fn = taskdata.fn_index[fnid]
            pn = self.status.pkg_fn[fn]
            version  = "%s:%s-%s" % self.status.pkg_pepvpr[fn]
            if pn not in depend_tree["pn"]:
                depend_tree["pn"][pn] = {}
                depend_tree["pn"][pn]["filename"] = fn
                depend_tree["pn"][pn]["version"] = version
            for dep in rq.runq_depends[task]:
                depfn = taskdata.fn_index[rq.runq_fnid[dep]]
                deppn = self.status.pkg_fn[depfn]
                dotname = "%s.%s" % (pn, rq.runq_task[task])
                if not dotname in depend_tree["tdepends"]:
                    depend_tree["tdepends"][dotname] = []
                depend_tree["tdepends"][dotname].append("%s.%s" % (deppn, rq.runq_task[dep]))
            if fnid not in seen_fnids:
                seen_fnids.append(fnid)
                packages = []

                depend_tree["depends"][pn] = []
                for dep in taskdata.depids[fnid]:
                    depend_tree["depends"][pn].append(taskdata.build_names_index[dep])

                depend_tree["rdepends-pn"][pn] = []
                for rdep in taskdata.rdepids[fnid]:
                        depend_tree["rdepends-pn"][pn].append(taskdata.run_names_index[rdep])

                rdepends = self.status.rundeps[fn]
                for package in rdepends:
                    depend_tree["rdepends-pkg"][package] = []
                    for rdepend in rdepends[package]:
                        depend_tree["rdepends-pkg"][package].append(rdepend)
                    packages.append(package)

                rrecs = self.status.runrecs[fn]
                for package in rrecs:
                    depend_tree["rrecs-pkg"][package] = []
                    for rdepend in rrecs[package]:
                        depend_tree["rrecs-pkg"][package].append(rdepend)
                    if not package in packages:
                        packages.append(package)

                for package in packages:
                    if package not in depend_tree["packages"]:
                        depend_tree["packages"][package] = {}
                        depend_tree["packages"][package]["pn"] = pn
                        depend_tree["packages"][package]["filename"] = fn
                        depend_tree["packages"][package]["version"] = version

        return depend_tree


    def generateDepTreeEvent(self, pkgs_to_build):
        """
        Create a task dependency graph of pkgs_to_build.
        Generate an event with the result
        """
        depgraph = self.generateDepTreeData(pkgs_to_build)
        bb.event.fire(bb.event.DepTreeGenerated(self.configuration.data, depgraph))

    def generateDotGraphFiles(self, pkgs_to_build):
        """
        Create a task dependency graph of pkgs_to_build.
        Save the result to a set of .dot files.
        """

        depgraph = self.generateDepTreeData(pkgs_to_build)

        # Prints a flattened form of package-depends below where subpackages of a package are merged into the main pn
        depends_file = file('pn-depends.dot', 'w' )
        print >> depends_file, "digraph depends {"
        for pn in depgraph["pn"]:
            fn = depgraph["pn"][pn]["filename"]
            version = depgraph["pn"][pn]["version"]
            print >> depends_file, '"%s" [label="%s %s\\n%s"]' % (pn, pn, version, fn)
        for pn in depgraph["depends"]:
            for depend in depgraph["depends"][pn]:
                print >> depends_file, '"%s" -> "%s"' % (pn, depend)
        for pn in depgraph["rdepends-pn"]:
            for rdepend in depgraph["rdepends-pn"][pn]:
                print >> depends_file, '"%s" -> "%s" [style=dashed]' % (pn, rdepend)
        print >> depends_file,  "}"
        bb.msg.plain("PN dependencies saved to 'pn-depends.dot'")

        depends_file = file('package-depends.dot', 'w' )
        print >> depends_file, "digraph depends {"
        for package in depgraph["packages"]:
            pn = depgraph["packages"][package]["pn"]
            fn = depgraph["packages"][package]["filename"]
            version = depgraph["packages"][package]["version"]
            if package == pn:
                print >> depends_file, '"%s" [label="%s %s\\n%s"]' % (pn, pn, version, fn)
            else:
                print >> depends_file, '"%s" [label="%s(%s) %s\\n%s"]' % (package, package, pn, version, fn)
            for depend in depgraph["depends"][pn]:
                print >> depends_file, '"%s" -> "%s"' % (package, depend)
        for package in depgraph["rdepends-pkg"]:
            for rdepend in depgraph["rdepends-pkg"][package]:
                print >> depends_file, '"%s" -> "%s" [style=dashed]' % (package, rdepend)
        for package in depgraph["rrecs-pkg"]:
            for rdepend in depgraph["rrecs-pkg"][package]:
                print >> depends_file, '"%s" -> "%s" [style=dashed]' % (package, rdepend)
        print >> depends_file,  "}"
        bb.msg.plain("Package dependencies saved to 'package-depends.dot'")

        tdepends_file = file('task-depends.dot', 'w' )
        print >> tdepends_file, "digraph depends {"
        for task in depgraph["tdepends"]:
            (pn, taskname) = task.rsplit(".", 1)
            fn = depgraph["pn"][pn]["filename"]
            version = depgraph["pn"][pn]["version"]
            print >> tdepends_file, '"%s.%s" [label="%s %s\\n%s\\n%s"]' % (pn, taskname, pn, taskname, version, fn)
            for dep in depgraph["tdepends"][task]:
                print >> tdepends_file, '"%s" -> "%s"' % (task, dep)
        print >> tdepends_file,  "}"
        bb.msg.plain("Task dependencies saved to 'task-depends.dot'")

    def buildDepgraph( self ):
        all_depends = self.status.all_depends
        pn_provides = self.status.pn_provides

        localdata = data.createCopy(self.configuration.data)
        bb.data.update_data(localdata)
        bb.data.expandKeys(localdata)

        def calc_bbfile_priority(filename):
            for (regex, pri) in self.status.bbfile_config_priorities:
                if regex.match(filename):
                    return pri
            return 0

        # Handle PREFERRED_PROVIDERS
        for p in (bb.data.getVar('PREFERRED_PROVIDERS', localdata, 1) or "").split():
            try:
                (providee, provider) = p.split(':')
            except:
                bb.msg.fatal(bb.msg.domain.Provider, "Malformed option in PREFERRED_PROVIDERS variable: %s" % p)
                continue
            if providee in self.status.preferred and self.status.preferred[providee] != provider:
                bb.msg.error(bb.msg.domain.Provider, "conflicting preferences for %s: both %s and %s specified" % (providee, provider, self.status.preferred[providee]))
            self.status.preferred[providee] = provider

        # Calculate priorities for each file
        for p in self.status.pkg_fn.keys():
            self.status.bbfile_priority[p] = calc_bbfile_priority(p)

    def buildWorldTargetList(self):
        """
         Build package list for "bitbake world"
        """
        all_depends = self.status.all_depends
        pn_provides = self.status.pn_provides
        bb.msg.debug(1, bb.msg.domain.Parsing, "collating packages for \"world\"")
        for f in self.status.possible_world:
            terminal = True
            pn = self.status.pkg_fn[f]

            for p in pn_provides[pn]:
                if p.startswith('virtual/'):
                    bb.msg.debug(2, bb.msg.domain.Parsing, "World build skipping %s due to %s provider starting with virtual/" % (f, p))
                    terminal = False
                    break
                for pf in self.status.providers[p]:
                    if self.status.pkg_fn[pf] != pn:
                        bb.msg.debug(2, bb.msg.domain.Parsing, "World build skipping %s due to both us and %s providing %s" % (f, pf, p))
                        terminal = False
                        break
            if terminal:
                self.status.world_target.add(pn)

            # drop reference count now
            self.status.possible_world = None
            self.status.all_depends    = None

    def interactiveMode( self ):
        """Drop off into a shell"""
        try:
            from bb import shell
        except ImportError, details:
            bb.msg.fatal(bb.msg.domain.Parsing, "Sorry, shell not available (%s)" % details )
        else:
            shell.start( self )

    def parseConfigurationFile( self, afile ):
        try:
            self.configuration.data = bb.parse.handle( afile, self.configuration.data )

            # Handle any INHERITs and inherit the base class
            inherits  = ["base"] + (bb.data.getVar('INHERIT', self.configuration.data, True ) or "").split()
            for inherit in inherits:
                self.configuration.data = bb.parse.handle(os.path.join('classes', '%s.bbclass' % inherit), self.configuration.data, True )

            # Nomally we only register event handlers at the end of parsing .bb files
            # We register any handlers we've found so far here...
            for var in data.getVar('__BBHANDLERS', self.configuration.data) or []:
                bb.event.register(var,bb.data.getVar(var, self.configuration.data))

            bb.fetch.fetcher_init(self.configuration.data)

            bb.event.fire(bb.event.ConfigParsed(self.configuration.data))

        except IOError, e:
            bb.msg.fatal(bb.msg.domain.Parsing, "Error when parsing %s: %s" % (afile, str(e)))
        except IOError:
            bb.msg.fatal(bb.msg.domain.Parsing, "Unable to open %s" % afile )
        except bb.parse.ParseError, details:
            bb.msg.fatal(bb.msg.domain.Parsing, "Unable to parse %s (%s)" % (afile, details) )

    def handleCollections( self, collections ):
        """Handle collections"""
        if collections:
            collection_list = collections.split()
            for c in collection_list:
                regex = bb.data.getVar("BBFILE_PATTERN_%s" % c, self.configuration.data, 1)
                if regex == None:
                    bb.msg.error(bb.msg.domain.Parsing, "BBFILE_PATTERN_%s not defined" % c)
                    continue
                priority = bb.data.getVar("BBFILE_PRIORITY_%s" % c, self.configuration.data, 1)
                if priority == None:
                    bb.msg.error(bb.msg.domain.Parsing, "BBFILE_PRIORITY_%s not defined" % c)
                    continue
                try:
                    cre = re.compile(regex)
                except re.error:
                    bb.msg.error(bb.msg.domain.Parsing, "BBFILE_PATTERN_%s \"%s\" is not a valid regular expression" % (c, regex))
                    continue
                try:
                    pri = int(priority)
                    self.status.bbfile_config_priorities.append((cre, pri))
                except ValueError:
                    bb.msg.error(bb.msg.domain.Parsing, "invalid value for BBFILE_PRIORITY_%s: \"%s\"" % (c, priority))

    def buildSetVars(self):
        """
        Setup any variables needed before starting a build
        """
        if not bb.data.getVar("BUILDNAME", self.configuration.data):
            bb.data.setVar("BUILDNAME", os.popen('date +%Y%m%d%H%M').readline().strip(), self.configuration.data)
        bb.data.setVar("BUILDSTART", time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime()), self.configuration.data)

    def matchFiles(self, buildfile):
        """
        Find the .bb files which match the expression in 'buildfile'.
        """

        bf = os.path.abspath(buildfile)
        try:
            os.stat(bf)
            return [bf]
        except OSError:
            (filelist, masked) = self.collect_bbfiles()
            regexp = re.compile(buildfile)
            matches = []
            for f in filelist:
                if regexp.search(f) and os.path.isfile(f):
                    bf = f
                    matches.append(f)
            return matches

    def matchFile(self, buildfile):
        """
        Find the .bb file which matches the expression in 'buildfile'.
        Raise an error if multiple files
        """
        matches = self.matchFiles(buildfile)
        if len(matches) != 1:
            bb.msg.error(bb.msg.domain.Parsing, "Unable to match %s (%s matches found):" % (buildfile, len(matches)))
            for f in matches:
                bb.msg.error(bb.msg.domain.Parsing, "    %s" % f)
            raise MultipleMatches
        return matches[0]

    def buildFile(self, buildfile, task):
        """
        Build the file matching regexp buildfile
        """

        fn = self.matchFile(buildfile)
        self.buildSetVars()

        # Load data into the cache for fn
        self.bb_cache = bb.cache.init(self)
        self.bb_cache.loadData(fn, self.configuration.data)      

        # Parse the loaded cache data
        self.status = bb.cache.CacheData()
        self.bb_cache.handle_data(fn, self.status)  

        # Tweak some variables
        item = self.bb_cache.getVar('PN', fn, True)
        self.status.ignored_dependencies = Set()
        self.status.bbfile_priority[fn] = 1

        # Remove external dependencies
        self.status.task_deps[fn]['depends'] = {}
        self.status.deps[fn] = []
        self.status.rundeps[fn] = []
        self.status.runrecs[fn] = []

        # Remove stamp for target if force mode active
        if self.configuration.force:
            bb.msg.note(2, bb.msg.domain.RunQueue, "Remove stamp %s, %s" % (task, fn))
            bb.build.del_stamp('do_%s' % task, self.status, fn)

        # Setup taskdata structure
        taskdata = bb.taskdata.TaskData(self.configuration.abort)
        taskdata.add_provider(self.configuration.data, self.status, item)

        buildname = bb.data.getVar("BUILDNAME", self.configuration.data)
        bb.event.fire(bb.event.BuildStarted(buildname, [item], self.configuration.event_data))

        # Execute the runqueue
        runlist = [[item, "do_%s" % self.configuration.cmd]]

        rq = bb.runqueue.RunQueue(self, self.configuration.data, self.status, taskdata, runlist)

        def buildFileIdle(server, rq, abort):

            if abort or self.cookerAction == cookerStop:
                rq.finish_runqueue(True)
            elif self.cookerAction == cookerShutdown:
                rq.finish_runqueue(False)
            failures = 0
            try:
                retval = rq.execute_runqueue()
            except runqueue.TaskFailure, fnids:
                for fnid in fnids:
                    bb.msg.error(bb.msg.domain.Build, "'%s' failed" % taskdata.fn_index[fnid])
                    failures = failures + 1
                retval = False
            if not retval:
                self.cookerIdle = True
                self.command.finishOfflineCommand()
                bb.event.fire(bb.event.BuildCompleted(buildname, targets, self.configuration.event_data, failures))
            return retval

        self.cookerIdle = False
        self.server.register_idle_function(buildFileIdle, rq)

    def buildTargets(self, targets):
        """
        Attempt to build the targets specified
        """

        # Need files parsed
        self.updateCache()

        targets = self.checkPackages(targets)

        def buildTargetsIdle(server, rq, abort):

            if abort or self.cookerAction == cookerStop:
                rq.finish_runqueue(True)
            elif self.cookerAction == cookerShutdown:
                rq.finish_runqueue(False)
            failures = 0
            try:
                retval = rq.execute_runqueue()
            except runqueue.TaskFailure, fnids:
                for fnid in fnids:
                    bb.msg.error(bb.msg.domain.Build, "'%s' failed" % taskdata.fn_index[fnid])
                    failures = failures + 1
                retval = False
            if not retval:
                self.cookerIdle = True
                self.command.finishOfflineCommand()
                bb.event.fire(bb.event.BuildCompleted(buildname, targets, self.configuration.event_data, failures))
            return retval

        self.buildSetVars()

        buildname = bb.data.getVar("BUILDNAME", self.configuration.data)
        bb.event.fire(bb.event.BuildStarted(buildname, targets, self.configuration.event_data))

        localdata = data.createCopy(self.configuration.data)
        bb.data.update_data(localdata)
        bb.data.expandKeys(localdata)

        taskdata = bb.taskdata.TaskData(self.configuration.abort)

        runlist = []
        for k in targets:
            taskdata.add_provider(localdata, self.status, k)
            runlist.append([k, "do_%s" % self.configuration.cmd])
        taskdata.add_unresolved(localdata, self.status)

        rq = bb.runqueue.RunQueue(self, self.configuration.data, self.status, taskdata, runlist)

        self.cookerIdle = False
        self.server.register_idle_function(buildTargetsIdle, rq)

    def updateCache(self):

        if self.cookerState == cookerParsed:
            return

        # Import Psyco if available and not disabled
        import platform
        if platform.machine() in ['i386', 'i486', 'i586', 'i686']:
            if not self.configuration.disable_psyco:
                try:
                    import psyco
                except ImportError:
                    bb.msg.note(1, bb.msg.domain.Collection, "Psyco JIT Compiler (http://psyco.sf.net) not available. Install it to increase performance.")
                else:
                    psyco.bind( self.parse_bbfiles )
            else:
                bb.msg.note(1, bb.msg.domain.Collection, "You have disabled Psyco. This decreases performance.")

        self.status = bb.cache.CacheData()

        ignore = bb.data.getVar("ASSUME_PROVIDED", self.configuration.data, 1) or ""
        self.status.ignored_dependencies = Set(ignore.split())

        for dep in self.configuration.extra_assume_provided:
            self.status.ignored_dependencies.add(dep)

        self.handleCollections( bb.data.getVar("BBFILE_COLLECTIONS", self.configuration.data, 1) )

        bb.msg.debug(1, bb.msg.domain.Collection, "collecting .bb files")
        bb.data.renameVar("__depends", "__base_depends", self.configuration.data)
        (filelist, masked) = self.collect_bbfiles()
        self.parse_bbfiles(filelist, masked)
        bb.msg.debug(1, bb.msg.domain.Collection, "parsing complete")

        self.buildDepgraph()

        self.cookerState = cookerParsed

    def checkPackages(self, pkgs_to_build):

        if len(pkgs_to_build) == 0:
            raise NothingToBuild

        if 'world' in pkgs_to_build:
            self.buildWorldTargetList()
            pkgs_to_build.remove('world')
            for t in self.status.world_target:
                pkgs_to_build.append(t)

        return pkgs_to_build

    def get_bbfiles( self, path = os.getcwd() ):
        """Get list of default .bb files by reading out the current directory"""
        contents = os.listdir(path)
        bbfiles = []
        for f in contents:
            (root, ext) = os.path.splitext(f)
            if ext == ".bb":
                bbfiles.append(os.path.abspath(os.path.join(os.getcwd(),f)))
        return bbfiles

    def find_bbfiles( self, path ):
        """Find all the .bb files in a directory"""
        from os.path import join

        found = []
        for dir, dirs, files in os.walk(path):
            for ignored in ('SCCS', 'CVS', '.svn'):
                if ignored in dirs:
                    dirs.remove(ignored)
            found += [join(dir,f) for f in files if f.endswith('.bb')]

        return found

    def collect_bbfiles( self ):
        """Collect all available .bb build files"""
        parsed, cached, skipped, masked = 0, 0, 0, 0
        self.bb_cache = bb.cache.init(self)

        files = (data.getVar( "BBFILES", self.configuration.data, 1 ) or "").split()
        data.setVar("BBFILES", " ".join(files), self.configuration.data)

        if not len(files):
            files = self.get_bbfiles()

        if not len(files):
            bb.msg.error(bb.msg.domain.Collection, "no files to build.")

        newfiles = []
        for f in files:
            if os.path.isdir(f):
                dirfiles = self.find_bbfiles(f)
                if dirfiles:
                    newfiles += dirfiles
                    continue
            newfiles += glob.glob(f) or [ f ]

        bbmask = bb.data.getVar('BBMASK', self.configuration.data, 1)

        if not bbmask:
            return (newfiles, 0)

        try:
            bbmask_compiled = re.compile(bbmask)
        except sre_constants.error:
            bb.msg.fatal(bb.msg.domain.Collection, "BBMASK is not a valid regular expression.")

        finalfiles = []
        for i in xrange( len( newfiles ) ):
            f = newfiles[i]
            if bbmask and bbmask_compiled.search(f):
                bb.msg.debug(1, bb.msg.domain.Collection, "skipping masked file %s" % f)
                masked += 1
                continue
            finalfiles.append(f)

        return (finalfiles, masked)

    def parse_bbfiles(self, filelist, masked):
        parsed, cached, skipped, error, total = 0, 0, 0, 0, len(filelist)
        for i in xrange(total):
            f = filelist[i]

            #bb.msg.debug(1, bb.msg.domain.Collection, "parsing %s" % f)

            # read a file's metadata
            try:
                fromCache, skip = self.bb_cache.loadData(f, self.configuration.data)
                if skip:
                    skipped += 1
                    bb.msg.debug(2, bb.msg.domain.Collection, "skipping %s" % f)
                    self.bb_cache.skip(f)
                    continue
                elif fromCache: cached += 1
                else: parsed += 1
                deps = None

                # Disabled by RP as was no longer functional
                # allow metadata files to add items to BBFILES
                #data.update_data(self.pkgdata[f])
                #addbbfiles = self.bb_cache.getVar('BBFILES', f, False) or None
                #if addbbfiles:
                #    for aof in addbbfiles.split():
                #        if not files.count(aof):
                #            if not os.path.isabs(aof):
                #                aof = os.path.join(os.path.dirname(f),aof)
                #            files.append(aof)

                self.bb_cache.handle_data(f, self.status)

            except IOError, e:
                error += 1
                self.bb_cache.remove(f)
                bb.msg.error(bb.msg.domain.Collection, "opening %s: %s" % (f, e))
                pass
            except KeyboardInterrupt:
                self.bb_cache.sync()
                raise
            except Exception, e:
                error += 1
                self.bb_cache.remove(f)
                bb.msg.error(bb.msg.domain.Collection, "%s while parsing %s" % (e, f))
            except:
                self.bb_cache.remove(f)
                raise
            finally:
                bb.event.fire(bb.event.ParseProgress(self.configuration.event_data, cached, parsed, skipped, masked, error, total))

        self.bb_cache.sync()
        if error > 0:
             raise ParsingErrorsFound

    def serve(self):

        if self.configuration.profile:
            try:
                import cProfile as profile
            except:
                import profile

            profile.runctx("self.server.serve_forever()", globals(), locals(), "profile.log")

            # Redirect stdout to capture profile information
            pout = open('profile.log.processed', 'w')
            so = sys.stdout.fileno()
            os.dup2(pout.fileno(), so)

            import pstats
            p = pstats.Stats('profile.log')
            p.sort_stats('time')
            p.print_stats()
            p.print_callers()
            p.sort_stats('cumulative')
            p.print_stats()

            os.dup2(so, pout.fileno())
            pout.flush()
            pout.close()
        else:
            self.server.serve_forever()
        
        bb.event.fire(CookerExit(self.configuration.event_data))
        
class CookerExit(bb.event.Event):
    """
    Notify clients of the Cooker shutdown
    """

    def __init__(self, d):
        bb.event.Event.__init__(self, d)

