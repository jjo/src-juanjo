#!/bin/sh
# $Id: jjotip-eval-comillas.sh,v 1.2 2004/10/23 14:38:28 jjo Exp $
# re-evaluacio'n de comillas... usable para bourne sh tambie'n
# [ab]uso del u'nico array que tiene (el viejo) bourne shell: $*
LUCA='"luquita ..." una instancia de "una CLASSe desconocida"'
eval set -- $LUCA
for i in "$@";do
	echo "$i"
done
