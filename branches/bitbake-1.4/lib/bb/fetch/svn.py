#!/usr/bin/env python
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
"""
BitBake 'Fetch' implementations

Classes for obtaining upstream sources for the
BitBake build tools.

Copyright (C) 2003, 2004  Chris Larson

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA. 

Based on functions from the base bb module, Copyright 2003 Holger Schurig
"""

import os, re
import bb
from   bb import data
from   bb.fetch import Fetch
from   bb.fetch import FetchError
from   bb.fetch import MissingParameterError

class Svn(Fetch):
    """Class to fetch a module or modules from svn repositories"""
    def supports(url, d):
        """Check to see if a given url can be fetched with svn.
           Expects supplied url in list form, as outputted by bb.decodeurl().
        """
        (type, host, path, user, pswd, parm) = bb.decodeurl(data.expand(url, d))
        return type in ['svn']
    supports = staticmethod(supports)

    def localpath(url, d):
        (type, host, path, user, pswd, parm) = bb.decodeurl(data.expand(url, d))
        if "localpath" in parm:
#           if user overrides local path, use it.
            return parm["localpath"]

        if not "module" in parm:
            raise MissingParameterError("svn method needs a 'module' parameter")
        else:
            module = parm["module"]
        if 'rev' in parm:
            revision = parm['rev']
        else:
            revision = ""

        date = Fetch.getSRCDate(d)

        return os.path.join(data.getVar("DL_DIR", d, 1),data.expand('%s_%s_%s_%s_%s.tar.gz' % ( module.replace('/', '.'), host, path.replace('/', '.'), revision, date), d))
    localpath = staticmethod(localpath)

    def go(self, d, urls = []):
        """Fetch urls"""
        if not urls:
            urls = self.urls

        localdata = data.createCopy(d)
        data.setVar('OVERRIDES', "svn:%s" % data.getVar('OVERRIDES', localdata), localdata)
        data.update_data(localdata)

        for loc in urls:
            (type, host, path, user, pswd, parm) = bb.decodeurl(data.expand(loc, localdata))
            if not "module" in parm:
                raise MissingParameterError("svn method needs a 'module' parameter")
            else:
                module = parm["module"]

            dlfile = self.localpath(loc, localdata)
            dldir = data.getVar('DL_DIR', localdata, 1)
#           if local path contains the svn
#           module, consider the dir above it to be the
#           download directory
#           pos = dlfile.find(module)
#           if pos:
#               dldir = dlfile[:pos]
#           else:
#               dldir = os.path.dirname(dlfile)

#           setup svn options
            options = []
            if 'rev' in parm:
                revision = parm['rev']
            else:
                revision = ""

            date = Fetch.getSRCDate(d)

            if "proto" in parm:
                proto = parm["proto"]
            else:
                proto = "svn"

            svn_rsh = None
            if proto == "svn+ssh" and "rsh" in parm:
                svn_rsh = parm["rsh"]

            tarfn = data.expand('%s_%s_%s_%s_%s.tar.gz' % (module.replace('/', '.'), host, path.replace('/', '.'), revision, date), localdata)
            data.setVar('TARFILES', dlfile, localdata)
            data.setVar('TARFN', tarfn, localdata)

            dl = os.path.join(dldir, tarfn)
            if os.access(dl, os.R_OK):
                bb.debug(1, "%s already exists, skipping svn checkout." % tarfn)
                continue

            # try to use the tarball stash
            if Fetch.try_mirror(d, tarfn):
                continue

            olddir = os.path.abspath(os.getcwd())
            os.chdir(data.expand(dldir, localdata))

            svnroot = host + path

            data.setVar('SVNROOT', svnroot, localdata)
            data.setVar('SVNCOOPTS', " ".join(options), localdata)
            data.setVar('SVNMODULE', module, localdata)
            svncmd = data.getVar('FETCHCOMMAND', localdata, 1)
            svncmd = "svn co -r {%s} %s://%s/%s" % (date, proto, svnroot, module)

            if revision:
                svncmd = "svn co -r %s %s://%s/%s" % (revision, proto, svnroot, module)
            if svn_rsh:
                svncmd = "svn_RSH=\"%s\" %s" % (svn_rsh, svncmd)

#           create temp directory
            bb.debug(2, "Fetch: creating temporary directory")
            bb.mkdirhier(data.expand('${WORKDIR}', localdata))
            data.setVar('TMPBASE', data.expand('${WORKDIR}/oesvn.XXXXXX', localdata), localdata)
            tmppipe = os.popen(data.getVar('MKTEMPDIRCMD', localdata, 1) or "false")
            tmpfile = tmppipe.readline().strip()
            if not tmpfile:
                bb.error("Fetch: unable to create temporary directory.. make sure 'mktemp' is in the PATH.")
                raise FetchError(module)

#           check out sources there
            os.chdir(tmpfile)
            bb.note("Fetch " + loc)
            bb.debug(1, "Running %s" % svncmd)
            myret = os.system(svncmd)
            if myret != 0:
                try:
                    os.rmdir(tmpfile)
                except OSError:
                    pass
                raise FetchError(module)

            os.chdir(os.path.join(tmpfile, os.path.dirname(module)))
#           tar them up to a defined filename
            myret = os.system("tar -czf %s %s" % (os.path.join(dldir,tarfn), os.path.basename(module)))
            if myret != 0:
                try:
                    os.unlink(tarfn)
                except OSError:
                    pass
#           cleanup
            os.system('rm -rf %s' % tmpfile)
            os.chdir(olddir)
        del localdata
