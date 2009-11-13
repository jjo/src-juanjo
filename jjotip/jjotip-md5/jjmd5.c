#include <stdio.h>
#include <unistd.h>
#include <openssl/md5.h>

/* 
 * Mini sumador MD5
 * Autor: JuanJo Ciarlante
 *
 * compilar con:
 * 	make jjmd5 LDLIBS=-lssl
 * usarlo:
 * 	./jjmd5 < /etc/profile
 *   compararlo con
 *  	md5sum  < /etc/profile
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation; either version 2 of the License, or (at your
 * option) any later version.  See <http://www.fsf.org/copyleft/gpl.txt>.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 * for more details.
 */
int main(void) {
	static unsigned char buff[4096];	/* arbitrariamente igual al tamanio de pagina del x86 */
	static unsigned char md5_result[16];	/* 128 bits */
	int nread;
	int i;
	MD5_CTX ctx;				/* almacena "estado" de esta instancia de MD5 */

	if (isatty(0)) { 
		fprintf(stderr, "usame por stdin, ej: \n\tjjmd5 < archivo\n");
		return 1;
	}
	/*==> Paso 1: Inicializar MD5_CTX */
	MD5_Init(&ctx);

	while ((nread=read(0, buff, sizeof (buff)))>0) {
	/*==> Paso 2 <n veces>: Actualizar suma MD5 */
		MD5_Update(&ctx, buff, nread);
	}
	/*==> Paso 3 (final): Obtener suma MD5 y mostrarla */
	MD5_Final(md5_result, &ctx); 
	for (i=0;i<16;i++) { printf ("%02hhx", md5_result[i]); }
	putchar('\n');
	return 0;
}
