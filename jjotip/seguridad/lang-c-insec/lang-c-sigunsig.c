#if 0         /* hacer saltear a gcc desde aqui ... */

CFLAGS=-g -Wall -W
TARGET=lang-c-sigunsig
all: $(TARGET)
clean: 
	rm -f $(TARGET)

ifneq (,)     #  hacer saltear a make desde aqui ...
#endif        /* ... retomar gcc  */

/* =====================================================================*/
/* 
 * Author: JuanJo <jjo@mendoza.gov.ar> based on gera's curse from CORE 
 * $Id: lang-c-sigunsig.c,v 1.2 2004/09/23 17:32:32 jjo Exp $
 *
 * selfcontained c+Makefile, bizarre build:
 *      $ make -f lang-c-sigunsig.c
 * use:
 *      $ ./lang-c-sigunsig
 */
#include <stdio.h>

#define TAB0 "     "
#define TAB  TAB0 TAB0 TAB0 TAB0
#define SHOW_SOURCE(expr) puts(TAB0 #expr); expr
#define SHOW_SOURCE_AND_EVAL_BOOL(expr) \
	do { fputs(TAB0 "(" #expr ") ?", stdout); getchar(); puts( (expr)? TAB "TRUE" : TAB "FALSE"); } while (0)

int main(void) {
	SHOW_SOURCE(int ivar=-1);
	SHOW_SOURCE(unsigned uvar=4);
	puts("");
	SHOW_SOURCE_AND_EVAL_BOOL(-1 > 4);
	SHOW_SOURCE_AND_EVAL_BOOL(ivar > uvar);
	SHOW_SOURCE_AND_EVAL_BOOL(-1 > uvar);
	SHOW_SOURCE_AND_EVAL_BOOL(-1 > 4u);
	SHOW_SOURCE(ivar=268435456);
	SHOW_SOURCE_AND_EVAL_BOOL(ivar*15<0);
	SHOW_SOURCE_AND_EVAL_BOOL(ivar*16==0);
	SHOW_SOURCE_AND_EVAL_BOOL(0x40000001*2<0);
	SHOW_SOURCE_AND_EVAL_BOOL(-99%10 < 0);
	return 0;
}
/* =====================================================================*/
/*
endif   # ... cerrar condicional de make
#*/
