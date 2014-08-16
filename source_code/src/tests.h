/*
 * tests.h
 *
 * Created: 12/04/2014 17:19:27
 *  Author: limpkin
 */ 


#ifndef TESTS_H_
#define TESTS_H_

#include "defines.h"

#ifdef TESTS_ENABLED
void afterHadLogoDisplayTests(void);
void beforeFlashInitTests(void);
void afterFlashInitTests(void);
void afterTouchInitTests(void);
#else
#define afterHadLogoDisplayTests()
#define beforeFlashInitTests()
#define afterFlashInitTests()
#define afterTouchInitTests()
#endif

#endif /* TESTS_H_ */
