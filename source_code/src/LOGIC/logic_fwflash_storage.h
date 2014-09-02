/* CDDL HEADER START
 *
 * The contents of this file are subject to the terms of the
 * Common Development and Distribution License (the "License").
 * You may not use this file except in compliance with the License.
 *
 * You can obtain a copy of the license at src/license_cddl-1.0.txt
 * or http://www.opensolaris.org/os/licensing.
 * See the License for the specific language governing permissions
 * and limitations under the License.
 *
 * When distributing Covered Code, include this CDDL HEADER in each
 * file and include the License file at src/license_cddl-1.0.txt
 * If applicable, add the following below this CDDL HEADER, with the
 * fields enclosed by brackets "[]" replaced with your own identifying
 * information: Portions Copyright [yyyy] [name of copyright owner]
 *
 * CDDL HEADER END
 */
/*! \file   logic_fwflash_storage.h
 *  \brief  Logic for storing/getting fw data in the dedicated flash storage
 *  Copyright [2014] [Mathieu Stephan]
 */


#ifndef LOGIC_FWFLASH_STORAGE_H_
#define LOGIC_FWFLASH_STORAGE_H_

#include <stdbool.h>
#include "defines.h"
#include "file_ids.h"

extern bool flashIsValid;

// Prototypes
RET_TYPE getStoredFileAddr(FileId_t fileId, uint16_t* addr);
char* readStoredStringToBuffer(uint8_t stringID);
RET_TYPE checkBundleVersion(void);

#endif /* LOGIC_FWFLASH_STORAGE_H_ */
