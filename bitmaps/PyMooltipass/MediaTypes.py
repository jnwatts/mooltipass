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

MEDIA_UNKN   = 0
MEDIA_BITMAP = 1
MEDIA_FONT   = 2
MEDIA_STRING = 3

MEDIA_TYPE_NAMES = {
    MEDIA_UNKN: 'unkn',
    MEDIA_BITMAP: 'bmap',
    MEDIA_FONT: 'font',
    MEDIA_STRING: 'string',
}

MEDIA_TYPE_PREFIXES = {
    MEDIA_UNKN: 'UNKNOWN_',
    MEDIA_BITMAP: 'BITMAP_',
    MEDIA_FONT: 'FONT_',
    MEDIA_STRING: 'STRING_',
}

def getMediaTypeNames():
    return MEDIA_TYPE_NAMES.values();

def getMediaTypeKeys():
    return MEDIA_TYPE_NAMES.keys();

def getMediaTypeKeyFromName(name):
    for key,value in MEDIA_TYPE_NAMES.viewitems():
        if value == name:
            return key;
    return MEDIA_UNKN;

def getMediaTypeNameFromKey(key):
    if not key in MEDIA_TYPE_NAMES:
        key = MEDIA_UNKN;
    return MEDIA_TYPE_NAMES[key];

def getMediaTypePrefixFromKey(key):
    if not key in MEDIA_TYPE_NAMES:
        key = MEDIA_UNKN;
    return MEDIA_TYPE_PREFIXES[key];

def getMediaTypePrefixFromName(name):
    return getMediaTypePrefixFromKey(getMediaTypeKeyFromName(name));
