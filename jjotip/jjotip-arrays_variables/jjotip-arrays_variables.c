/*
 * Variable sized array in C, in response to Groucho's:
 *    http://www.lugmen.org.ar/pipermail/lug-devel/2005-December/000670.html
 * 
 * Autor: JuanJo Ciarlante ... jjo () mendoza gov ar
 * Licencia: GPLv2
 *
 * Compile with
    make CFLAGS=-Wall jjotip-arrays_variables

 * NOTES:
 * - the construction (sizeof(vector)/sizeof(*vector)) yields the number of
 *   elements :-)
 * - array[][] initializer is correctly done as  {  {element1},  {element2}, ... };
 */
#include <stdio.h>
#include <sys/types.h>

typedef const u_int16_t fragmentos_t[][2];
static fragmentos_t fragmentos_unsupported={ {0, 1} };
static fragmentos_t fragmentos_foo={ {0,17},  {19,15},  {35,12},  {47,12} };
static fragmentos_t fragmentos_bar={ {0,19},  {19,16},  {35,16},  {51,9},  {11,23} };

static fragmentos_t *(p_fragmento)=&fragmentos_unsupported;
static fragmentos_t *tabla_fragmentos[] =
{
  &fragmentos_unsupported,
  &fragmentos_foo,
  &fragmentos_bar
};

static const u_int16_t tabla_n_fragmentos[] =
{
  sizeof(fragmentos_unsupported)/(sizeof(*fragmentos_unsupported)),
  sizeof(fragmentos_foo)/(sizeof(*fragmentos_foo)),
  sizeof(fragmentos_bar)/(sizeof(*fragmentos_bar)),
};

int main(void)
{
	int i, n;
	for (i=0;i<(sizeof(tabla_n_fragmentos)/sizeof(*tabla_n_fragmentos));i++) {
		n=tabla_n_fragmentos[i];
		p_fragmento=tabla_fragmentos[i];
		printf ("tabla_n_fragmentos[%d]=%d ", i, n);
		printf (", ultimo fragmento={%d,%d}\n", (*p_fragmento)[n-1][0], (*p_fragmento)[n-1][1]);
	}
	return 0;
}
