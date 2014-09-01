#!/usr/bin/env python
#
# Copyright (c) 2014 Darran Hunt (darran [at] hunt dot net dot nz)
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
# Portions Copyright 2014 Josh Watts (josh [at] sroz dot net)


#
# Bundle a collection of bitmaps into a flat image with indices that can
# be imported into the SPI flash media region on the mooltipass
#
# Note: fonts are expected to have the word "font" in their filename
#

import os;
import sys;
import md5;
import yaml;
from optparse import OptionParser;
from struct import pack,unpack;
from array import array

from PyMooltipass.Bundle import *;

parser = OptionParser(usage = '''usage: %prog [options] [zero or more resource file]

- One of --create, --enum, --list, or --extract must be given.
- If no resource file is given, --file must specify a valid bundle file to extract or list
- Each resource file may contain any or all types of files: bitmaps and fonts may be in separate files, and/or bitmaps may be brought in from multiple files.
- --file accepts - as STDIN or STDOUT depending on mode

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

parser.add_option('-f', '--file', help='name of bundle file to operate on (default: -)', dest='filename', default='-')
parser.add_option('-c', '--create', help='create mode', action='store_true', dest='create_mode', default=False);
parser.add_option('-e', '--enum', help='enum mode', action='store_true', dest='enum_mode', default=False)
parser.add_option('-x', '--extract', help='extract mode', action='store_true', dest='extract_mode', default=False);
parser.add_option('-t', '--list', help='list mode', action='store_true', dest='list_mode', default=False);
parser.add_option('-d', '--depends', help='dependency mode', action='store_true', dest='depends_mode', default=False);
parser.add_option('-v', '--verbose', help='verbosely list files', dest='verbose', action='store_true', default=False);
parser.add_option('-5', '--md5', help='list md5sum for entries in bundle', dest='show_md5', action='store_true', default=False);
(options, args) = parser.parse_args()

MODE_INVALID = 0
MODE_CREATE = 1
MODE_ENUM = 2
MODE_EXTRACT = 3
MODE_LIST = 4
MODE_DEPENDS = 5

def readResourceFile(filename):
    fd = open(filename, 'r');
    result = yaml.load(fd);
    fd.close();
    return result;

def createBundle(options, args):
    bundle = Bundle(verbose=options.verbose, calculateHash=options.show_md5);

    for filename in args:
        resources = readResourceFile(filename);
        
        # Extract version from resource file, keep highest number found
        if 'version' in resources:
            if resources['version'] > bundle.getVersion():
                bundle.setVersion(resources['version']);

        # Extract media files from resource file
        for mediaType in getMediaTypeNames():
            if mediaType in resources:
                for name, filename in resources[mediaType]:
                    #print "{}: {} -> {}\n".format(mediaType, name, filename);
                    bundle.addFile(mediaType, name, filename);

    if len(bundle) <= 0:
        raise Exception('Cowardly refusing to create empty bundle');

    if options.filename == '-':
        fd = sys.stdout;
    else:
        fd = open(options.filename, 'w');

    if options.create_mode:
        # Write bundle to file
        bundle.tofile(fd);
    elif options.enum_mode:
        # Write enum to file
        fd.write(bundle.toEnumString());

    if not options.filename == '-':
        fd.close();

    return 0;


def main():
    result = 0;
    mode = MODE_INVALID;
    mode_count = 0;

    if options.create_mode:
        mode = MODE_CREATE;
        mode_count += 1;
    if options.extract_mode:
        mode = MODE_EXTRACT;
        mode_count += 1;
    if options.list_mode:
        mode = MODE_LIST;
        mode_count += 1;
    if options.enum_mode:
        mode = MODE_ENUM;
        mode_count += 1;
    if options.depends_mode:
        mode = MODE_DEPENDS;
        mode_count += 1;

    # Validate selected mode
    if mode_count == 0:
        result = 1;
        raise Exception("One of --create, --enum, --extract, --list or --depends must be specified");
    if mode_count > 1:
        result = 1;
        raise Exception("Only one of --create, --enum, --extract, --list or --depends must be specified");

    # Perform selected action
    if mode == MODE_CREATE or mode == MODE_ENUM:
        result = createBundle(options, args);
    elif mode == MODE_EXTRACT:
        result = 1;
        raise Exception("--extract is not yet implemented");
    elif mode == MODE_LIST:
        result = 1;
        raise Exception("--list is not yet implemented");
    elif mode == MODE_DEPENDS:
        result = createDepends(options, args);

    return result;

if __name__ == "__main__":
    sys.exit(main());
