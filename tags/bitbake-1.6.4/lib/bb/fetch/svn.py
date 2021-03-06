# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
"""
BitBake 'Fetch' implementations

This implementation is for svn. It is based on the cvs implementation.

"""

# Copyright (C) 2004 Marcin Juszkiewicz
#
#   Classes for obtaining upstream sources for the
#   BitBake build tools.
#   Copyright (C) 2003, 2004  Chris Larson
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
#
# Based on functions from the base bb module, Copyright 2003 Holger Schurig

import os, re
import sys
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

        if 'srcdate' in parm:
            date = parm['srcdate']

        if revision:
            date = ""

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

            date = Fetch.getSRCDate(d)

            if 'srcdate' in parm:
                date = parm['srcdate']

            revision = ""
            if 'rev' in parm:
                revision = parm['rev']
            
            if revision:
                options.append("-r %s" % revision)
            elif date != "now":
                options.append("-r {%s}" % date)

            if revision:
                date = ""


            if user:
                options.append("--username %s" % user)

            if pswd:
                options.append("--password %s" % pswd)

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

            # try to use the tarball stash
            if Fetch.check_for_tarball(d, tarfn, dldir, date):
                bb.debug(1, "%s already exists or was mirrored, skipping svn checkout." % tarfn)
                continue

            olddir = os.path.abspath(os.getcwd())
            os.chdir(data.expand(dldir, localdata))

            svnroot = host + path

            data.setVar('SVNROOT', "%s://%s/%s" % (proto, svnroot, module), localdata)
            data.setVar('SVNCOOPTS', " ".join(options), localdata)
            data.setVar('SVNMODULE', module, localdata)
            svncmd = data.getVar('FETCHCOMMAND', localdata, 1)
            svnupcmd = data.getVar('UPDATECOMMAND', localdata, 1)

            if svn_rsh:
                svncmd = "svn_RSH=\"%s\" %s" % (svn_rsh, svncmd)
                svnupcmd = "svn_RSH=\"%s\" %s" % (svn_rsh, svnupcmd)

            pkg = data.expand('${PN}', d)
            pkgdir = os.path.join(data.expand('${SVNDIR}', localdata), pkg)
            moddir = os.path.join(pkgdir, module)
            bb.debug(2, "Fetch: checking for module directory '%s'" % moddir)

            if os.access(os.path.join(moddir, '.svn'), os.R_OK):
                bb.note("Update " + loc)
                # update sources there
                os.chdir(moddir)
                bb.debug(1, "Running %s" % svnupcmd)
                myret = os.system(svnupcmd)
            else:
                bb.note("Fetch " + loc)
#               check out sources there
                bb.mkdirhier(pkgdir)
                os.chdir(pkgdir)
                bb.debug(1, "Running %s" % svncmd)
                myret = os.system(svncmd)
            if myret != 0:
                raise FetchError(module)

            os.chdir(pkgdir)
#           tar them up to a defined filename
            myret = os.system("tar -czf %s %s" % (os.path.join(dldir,tarfn), os.path.basename(module)))
            if myret != 0:
                try:
                    os.unlink(tarfn)
                except OSError:
                    pass
            os.chdir(olddir)
        del localdata
