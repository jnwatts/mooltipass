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

import os;
import sys;
import md5;

from MediaTypes import *;

class BundleFile:
    """Holds information related to a file entry in a bundle"""
    mediaType = 0;
    name = "";
    filename = "";
    filehash = "";
    filesize = "";

    def __init__(self, mediaType, name, filename, calculateHash=False):
        if isinstance(mediaType, str):
            mediaType = getMediaTypeKeyFromName(mediaType);
        self.mediaType = mediaType;
        self.name = getMediaTypePrefixFromKey(mediaType) + name;
        self.filename = filename;
        data = self.getData();
        if calculateHash:
            m = md5.new();
            m.update(data);
            self.filehash = m.hexdigest();
        self.filesize = len(data);

    def getMediaType(self):
        return self.mediaType;

    def getName(self):
        return self.name;

    def getFilename(self):
        return self.filename;

    def getFilehash(self):
        return self.filehash;

    def getFilesize(self):
        return self.filesize;

    def dumps(self):
        return "size {} bytes, {} {} {}".format(self.filesize, self.name, self.filename, self.filehash);

    def getData(self):
        data = None;
        if self.mediaType == MEDIA_STRING:
            # Special case for strings: "filename" is the data
            data = bytearray(self.filename.strip());
            data.append('\0');
        else:
            fd = open(self.filename, 'rb');
            data = fd.read();
            fd.close();
        return data;

    def tofile(self, fd):
        fd.write(self.getData());

