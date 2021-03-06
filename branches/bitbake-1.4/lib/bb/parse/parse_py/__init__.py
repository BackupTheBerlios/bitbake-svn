#!/usr/bin/env python
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
"""
BitBake Parsers

File parsers for the BitBake build tools.

Copyright (C) 2003, 2004  Chris Larson
Copyright (C) 2003, 2004  Phil Blundell

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
__version__ = '1.0'

__all__ = [ 'ConfHandler', 'BBHandler']

import ConfHandler
import BBHandler
