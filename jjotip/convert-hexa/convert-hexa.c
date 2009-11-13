/** 
 * \file convert-hexa.c converts from hexa digits to buffer
 * \author Juanjo Ciarlante,  jjo (.) mendoza.gov.ar
 * License: GPLv2+
 */
#include <stdio.h>
#include <string.h>

/** 256 char array for digit->value mapping */
char map_hexa_to_value[256];

/** Initializes map_hexa_to_value array so that map_hexa_to_value[digit] yields
 * its 4bit value, else -1
 * \param array the 256 elem array to initialize
 * \return void
 */
void init_map_hexa_to_value(char array[256]) {
	int i;
	memset(array, -1, 256);
	for (i='0'; i<='9';i++) array[i]=i-'0'+0;
	for (i='a'; i<='f';i++) array[i]=i-'a'+10;
	for (i='A'; i<='F';i++) array[i]=i-'A'+10;
}

/**
 * Converts hexa 2 digits to bytes
 * \param hexa 2-char array with hexa digits
 * \return unsigned byte value or less than 0 if invalid hexa digits were passed
 */
static inline int hexa_to_byte(const unsigned char hexa[2]) {
	return map_hexa_to_value[hexa[0]]*16+map_hexa_to_value[hexa[1]];
}
/**
 * Converts a hexa string with len bytes to their value
 * \param buf destination buffer
 * \param size size of buf
 * \param str hexa string
 * \param len string len of str
 */ 
void *hexa_to_mem(unsigned char *buf, int size, const unsigned char *str, int len) {
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

/** Just a simple test, will convert str[] variable to its value and
 * print it to stdout
 */
int main(void) {
	unsigned char str[]="6a6a6f2052756c657a00";
	unsigned char buf[256]="";
	char *ret;
	init_map_hexa_to_value(map_hexa_to_value);
	ret=hexa_to_mem(buf, sizeof(buf),str, strlen((char*)str));
	printf("%s\n", ret? ret : "<NULL>");
	return 0;
}
