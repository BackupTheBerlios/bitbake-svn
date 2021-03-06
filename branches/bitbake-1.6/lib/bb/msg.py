# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
"""
BitBake 'msg' implementation

Message handling infrastructure for bitbake

"""

# Copyright (C) 2006        Richard Purdie
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

import sys, os, re, bb
from bb import utils

debug_level = 0

verbose = False

domain = bb.utils.Enum('Depends', 'Provider', 'Build', 'Parsing', 'Collection')

#
# Message control functions
#

def set_debug_level(level):
    bb.msg.debug_level = level

def set_verbose(level):
    bb.msg.verbose = level

#
# Message handling functions
#

def debug(level, domain, msg, fn = None):
    std_debug(level, msg)

def note(level, domain, msg, fn = None):
    if level == 1 or verbose:
        std_note(msg)

def warn(domain, msg, fn = None):
    std_warn(msg)

def error(domain, msg, fn = None):
    std_error(msg)

def fatal(domain, msg, fn = None):
    std_fatal(msg)

#
# Compatibility functions for the original message interface
#
def std_debug(lvl, msg):
    if debug_level >= lvl:
        print 'DEBUG: ' + msg

def std_note(msg):
    print 'NOTE: ' + msg

def std_warn(msg):
    print 'WARNING: ' + msg

def std_error(msg):
    print 'ERROR: ' + msg

def std_fatal(msg):
    print 'ERROR: ' + msg
    sys.exit(1)

