/* 
 * convert-hexa: converts from hexa digits to buffer w/o library functions (example program)
 *
 * Author: Juanjo Ciarlante,  jjo (.) mendoza.gov.ar
 * License: GPLv2+
 */
#include <stdio.h>
#include <string.h>
#include <assert.h>


static char str_from_hexa[256];

static void init_str_from_hexa(char array[256]) {
	int i;
	memset(array, -1, 256);
	for (i='0'; i<='9';i++) array[i]=i-'0'+0;
	for (i='a'; i<='f';i++) array[i]=i-'a'+10;
	for (i='A'; i<='F';i++) array[i]=i-'A'+10;
}

static inline int hexa_to_byte(const unsigned char hexa[2]) {
	return str_from_hexa[hexa[0]]*16+str_from_hexa[hexa[1]];
}
static void *hexa_to_mem(unsigned char *buf, int size, const unsigned char *str, int len) {
	int i, ret;
	if (len%2) return NULL;
	len/=2;
	if (size<len) len=size;
	for(i=0;i<len;i++) {
		ret=hexa_to_byte(str+i*2);	
		if (ret<0) return NULL;
		buf[i]=ret;
	}
	return buf;
}

int main(void) {
	unsigned char str[]="6a6a6f2052756c657a00";
	unsigned char buf[256]="";
	char *ret;
	init_str_from_hexa(str_from_hexa);
	ret=hexa_to_mem(buf, sizeof(buf),str, strlen((char*)str));
	printf("%s\n", ret? ret : "<NULL>");
	return 0;
}
