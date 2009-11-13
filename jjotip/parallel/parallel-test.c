/* Saca un byte por el port paralelo, incluyendo se~nalizacio'n de hardware (STROBE 1->0) */
/* Autor: JuanJo Ciarlante   jjo (.) mendoza.gov.ar */
/* Licencia: GPLv2+ */

/*    make CC="diet gcc -O2" parallel-test */
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/io.h>

#define LP0_DATA	0x378
#define LP0_STATUS	LP0_DATA+1
#define LP0_CONTROL	LP0_DATA+2


#define PARPORT_STROBE	0x01
#define PARPORT_DIRECTION	0x20


int main(void)
{
	unsigned short data = 0x77;
	unsigned short ctl_bak, ctl;

	if (ioperm(LP0_DATA,3,1)) {
		perror("ioperm (root please...)");
		return 1;
	}

	ctl_bak=inb(LP0_CONTROL);
	ctl=ctl_bak & ~PARPORT_DIRECTION;	/* apaga el bit DIRECTION para ... */
	outb(ctl                  , LP0_CONTROL); /* ... forzar sentido "out" */
	outb(data                 , LP0_DATA);	/* output de data */
	outb(ctl |  PARPORT_STROBE, LP0_CONTROL);	/* STROBE=1 */
	outb(ctl & ~PARPORT_STROBE, LP0_CONTROL);	/* STROBE=0 (para "sync" hacia impresora)*/
	outb(ctl_bak              , LP0_CONTROL);	/* restaura CTL original */
	return 0;
}
