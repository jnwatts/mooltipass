#!/usr/bin/env python
#
# Copyright (c) 2014 Josh Watts (josh [at] sroz dot net)
# All rights reserved.
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at src/license_cddl-1.0.txt
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at src/license_cddl-1.0.txt
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END


import os;
import sys;
import md5;
import yaml;
from optparse import OptionParser;
from struct import pack,unpack;
from array import array

from PyMooltipass.MediaTypes import *;

parser = OptionParser(usage = '''usage: %prog [options] [zero or more resource file]

Example YAML formatted resource file:

{
    "bmap":
    [
        ["BITMAP_NAME", "bitmap_filename.img"],
    ],
    "font":
    [
        ["FONT_NAME", "font_filename.img"],
    ],
    "string":
    [
        ["STRING_NAME", "Some string text..."],
    ],
} ''');

parser.add_option('-f', '--file', help='name of file to operate on (default: -)', dest='filename', default='-')
parser.add_option('-d', '--depends', help='dependency mode', action='store_true', dest='depends_mode', default=False);
parser.add_option('-v', '--verbose', help='verbosely list files', dest='verbose', action='store_true', default=False);
(options, args) = parser.parse_args()

MODE_INVALID = 0
MODE_DEPENDS = 1

def readResourceFile(filename):
    fd = open(filename, 'r');
    result = yaml.load(fd);
    fd.close();
    return result;

def createDepends(options, args):
    if options.filename == '-':
        fd = sys.stdout;
    else:
        fd = open(options.filename, 'w');
    
    for filename in args:
        resources = readResourceFile(filename);

        # Extract media files from resource file (skip strings)
        for mediaType in getMediaTypeNames():
            if mediaType in resources and not mediaType == getMediaTypeNameFromKey(MEDIA_STRING):
                for name, filename in resources[mediaType]:
                    if os.path.isfile(filename):
                        fd.write('{}\n'.format(filename));
                        if options.verbose:
                            print filename;

    if not options.filename == '-':
        fd.close();

    return 0;


def main():
    result = 0;
    mode = MODE_INVALID;
    mode_count = 0;

    if options.depends_mode:
        mode = MODE_DEPENDS;
        mode_count += 1;

    # Validate selected mode
    if mode_count == 0:
        result = 1;
        raise Exception("One of --depends must be specified");
    if mode_count > 1:
        result = 1;
        raise Exception("Only one of --depends must be specified");

    # Perform selected action
    if mode == MODE_DEPENDS:
        result = createDepends(options, args);

    return result;

if __name__ == "__main__":
    sys.exit(main());
