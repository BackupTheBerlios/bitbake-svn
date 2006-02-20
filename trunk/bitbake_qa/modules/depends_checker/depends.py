# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
#
# Copyright (C)       2005 Holger Hans Peter Freyther
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
#   Neither the name Holger Hans Peter Freyther nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from bittest import TestItem
from bb      import data

class TestCase:
    """
    Check if native packages have non native RDEPENDS
    """

    def __init__(self):
        pass

    def test(self,file_name, file_data):
        """
        Check if the RDEPENDS of a native package includes
        non native packages
        """
        if data.inherits_class("native", file_data):
            copy = data.createCopy(file_data)

            # add the package name to overrides and update the data
            pn = data.getVar('PN', copy, True)
            ov = data.getVar('OVERRIDES', copy, True)
            data.setVar('OVERRIDES', '%s:%s' % (pn,ov), copy )
            data.update_data(copy)

            rdepends = data.getVar('RDEPENDS', copy, True).strip()
            rdepends = rdepends.split(' ')
            for rdepend in rdepends:
                if len(rdepend.strip()) != 0 and not "-native" in rdepend:
                    return TestItem(file_name,False,"Native package is RDEPENDing on non native package '%s'" % rdepend)

    def test_name(self):
        """
        Retutnr a name for the test
        """
        return "RDEPEND checker for native packages"
