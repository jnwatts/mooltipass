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
/*!  \file     gui_credentials_functions.c
*    \brief    General user interface - credentials functions
*    Created:  22/6/2014
*    Author:   Mathieu Stephan
*/
#include "touch_higher_level_functions.h"
#include "gui_screen_functions.h"
#include "gui_basic_functions.h"
#include "node_mgmt.h"
#include "defines.h"
#include "oledmp.h"
#include "anim.h"
#include "gui.h"


#define USE_CONFIRM_SCREEN_FOR_SINGLE_CREDENTIAL

//TODO: These should be moved to a suitable common location
#define SCREEN_MARGIN_Y 4
#define SCREEN_MARGIN_X 0
#define SCREEN_HEIGHT 64
#define SCREEN_WIDTH 256
#define SCREEN_MAX_Y SCREEN_HEIGHT - 1
#define SCREEN_MAX_X SCREEN_WIDTH - 1
#define LINE_HEIGHT 12


/*! \fn     guiAskForLoginSelect(mgmtHandle* h, pNode* p, cNode* c, uint16_t parentNodeAddress)
*   \brief  Ask for user login selection / approval
*   \param  h                   Pointer to management handle
*   \param  p                   Pointer to a parent node
*   \param  c                   Pointer to a child node
*   \param  parentNodeAddress   Address of the parent node
*   \return Valid child node address or 0 otherwise
*/
uint16_t guiAskForLoginSelect(mgmtHandle* h, pNode* p, cNode* c, uint16_t parentNodeAddress)
{
    uint16_t temp_child_address;
    uint16_t addresses[4];
    uint8_t led_mask;
    int8_t i = 0;
    int8_t j;
    
    // Read the parent node
    if (readParentNode(h, p, parentNodeAddress) != RETURN_OK)
    {
        return NODE_ADDR_NULL;
    }
    
    // Read child address
    temp_child_address = p->nextChildAddress;
    
    // Check if there are stored credentials
    if (temp_child_address == NODE_ADDR_NULL)
    {
        return NODE_ADDR_NULL;
    }
    
    // Read child node
    if (readChildNode(h, c, temp_child_address) != RETURN_OK)
    {
        return NODE_ADDR_NULL;
    }
    
#ifdef USE_CONFIRM_SCREEN_FOR_SINGLE_CREDENTIAL // Saves 68 bytes
    // Check if there's only one child, that's a confirmation screen
    if (c->nextChildAddress == NODE_ADDR_NULL)
    {
        confirmationText_t temp_conf_text;
        
        // Prepare asking confirmation screen
        temp_conf_text.line1 = PSTR("Confirm login for");
        temp_conf_text.line2 = (char*)p->service;
        temp_conf_text.line3 = PSTR("with these credentials:");
        temp_conf_text.line4 = (char*)c->login;
        
        // Prompt user for confirmation
        if(guiAskForConfirmation(4, &temp_conf_text) != RETURN_OK)
        {
            temp_child_address = NODE_ADDR_NULL;
        }
        // Get back to other screen
        guiGetBackToCurrentScreen();
        return temp_child_address;
    }
    else
#endif
    {
        uint8_t action_chosen = FALSE;
        
        while (action_chosen != TRUE)
        {
            // Draw asking bitmap
            oledClear();
            oledBitmapDrawFlash(0, 0, BITMAP_LOGIN, 0);
            
            // Write domain name on screen
            oledPutstrXY(0, 24, OLED_CENTRE, (char*)p->service);
            
            // Clear led_mask
            led_mask = 0;

            // List logins on screen
            while ((temp_child_address != NODE_ADDR_NULL) && (i < 4))
            {
                // Read child node to get login
                if (readChildNode(h, c, temp_child_address) != RETURN_OK)
                {
                    return NODE_ADDR_NULL;
                }

                if (i == 0)
                {
                    // Cover left arrow if there's no predecessor
                    if (c->prevChildAddress == NODE_ADDR_NULL)
                    {
                        led_mask |= LED_MASK_LEFT;
                        oledFillXY(60, 24, 22, 18, 0x00);
                    }
                }

                // Print login on screen
                int leftRight = (i & 0x01);
                int topBot = (i & 0x02 >> 1);
                oledPutstrXY(
                        /* X */ SCREEN_MAX_X*leftRight, // 0, MAX_X
                        /* Y */ (SCREEN_HEIGHT - LINE_HEIGHT)*topBot + SCREEN_MARGIN_Y*(1-(2*topBot)), // MARGIN_Y, HEIGHT - LINE_HEIGHT - MARGIN_Y
                        /* Orienation */ leftRight, // OLED_LEFT == 0, OLED_RIGHT == 1
                        (char*)c->login);

                // Store address in array, fetch next address
                addresses[i] = temp_child_address;
                temp_child_address = c->nextChildAddress;
                i++;
            }

            // Update led_mask & bitmap
            if ((i < 4) || (c->nextChildAddress == NODE_ADDR_NULL))
            {
                led_mask |= LED_MASK_RIGHT;
                oledFillXY(174, 24, 22, 18, 0x00);
            }

            for (j = i; j < 4; j++)
            {
                led_mask |= (1 << j);
            }
            
            // Display picture
            oledFlipBuffers(0,0);
            
            // Set temp_child_address to last address
            temp_child_address = addresses[i-1];
            
            // Get touched quarter and check its validity
            j = getTouchedPositionAnswer(led_mask);
            if (j == -1)
            {
                // Time out, return nothing
                temp_child_address = NODE_ADDR_NULL;
                action_chosen = TRUE;
            }
            else if (j < i)
            {
                temp_child_address = addresses[j];
                action_chosen = TRUE;
            }
            else if (j == TOUCHPOS_LEFT)
            {
                // Get back to the initial child
                while ((i--) > 1)
                {
                    temp_child_address = c->prevChildAddress;
                    readChildNode(h, c, temp_child_address);
                }
                // If there is a previous child, go back 4 indexes
                if (c->prevChildAddress != NODE_ADDR_NULL)
                {
                    i = 4;
                    while(i--)
                    {
                        temp_child_address = c->prevChildAddress;
                        readChildNode(h, c, temp_child_address);
                    }
                }
                i = 0;
            }
            else if ((j == TOUCHPOS_RIGHT) && (i == 4) && (c->nextChildAddress != NODE_ADDR_NULL))
            {
                // If there are more nodes to display
                temp_child_address = c->nextChildAddress;
                i = 0;
            }
            else
            {
                // Wrong position, get back to the initial child
                while ((i--) > 1)
                {
                    temp_child_address = c->prevChildAddress;
                    readChildNode(h, c, temp_child_address);
                }
            }
        }
        
        // Get back to other screen
        guiGetBackToCurrentScreen();
    }

    return temp_child_address;
}
