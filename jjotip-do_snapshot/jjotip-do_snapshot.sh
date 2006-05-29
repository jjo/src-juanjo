#!/bin/bash
# Author: JuanJo Ciarlante: jjo // mendoza.gov.ar
# License: GPLv2+
#
# Construye un dispositivo snapshot ESCRIBIBLE (/dev/mapper/snap) en
# base a otro real READONLY (no debe estar montado).
# Para e'sto usa device mapper (dm-mod) haciendo los sigs. pasos:
# %1% Crea una proyeccion lineal completa del dispositivo original
#     en /dev/mapper/orig
# %2% Crea un loop device $(SNAP_DEV) para almacenar los bloques que se 
#     cambien usando un arch. temporal ($SNAP_FILE)
#     Ver archivo ./dmsetup-orig.table ($TABLE1)
# %3% Crea el snapshot /dev/mapper/snap desde /dev/mapper/orig
#     Ver archivo ./dmsetup-snap.table ($TABLE2)
#
# Ver discusión en http://www.lugmen.org.ar/pipermail/lug-list/2006-May/041507.html
#
# CONFIGURAR! estas dos vars:
ORIG_DEV=/dev/hdxx_EDITAME ## ej: /dev/hda10, /dev/sda5
SNAP_FILE=/tmp/snap.img
#
SNAP_SIZE=10000 #10Mb
SNAP_BLOCKSIZE=4
TABLE1=dmsetup-orig.table
TABLE2=dmsetup-snap.table
#ME_GUSTA_LA_ADENALINA="--noopencount"
#

ORIG_SIZE=$(blockdev --getsize $ORIG_DEV)
SNAP_DEV=$(losetup -f) #1er loop dev sin uso
#
modprobe dm-mod || exit 1
which dmsetup || exit 1
# Construye las tablas para dmsetup
echo "Creando $TABLE1 y $TABLE2"
echo 0 $ORIG_SIZE linear $ORIG_DEV 0 > $TABLE1
echo 0 $ORIG_SIZE snapshot $ORIG_DEV $SNAP_DEV p $((SNAP_BLOCKSIZE*2))  > $TABLE2
crea_snap() {
	## %1%
	dmsetup remove orig 2>/dev/null
	dmsetup -r $ME_GUSTA_LA_ADENALINA create orig < $TABLE1 || exit 1

	## %2%
	losetup -d $SNAP_DEV 2>/dev/null
	rm -f $SNAP_FILE
	dd if=/dev/zero of=$SNAP_FILE bs=1k seek=$SNAP_SIZE count=0 ## define tama~o final
	dd if=/dev/zero of=$SNAP_FILE conv=notrunc bs=1k count=4 ## limpia 1er bloque
	losetup $SNAP_DEV $SNAP_FILE || exit 1

	#blocksize medido en 512
	## %3%
	dmsetup remove snap 2>/dev/null
	dmsetup $ME_GUSTA_LA_ADENALINA create snap < $TABLE2 || exit 1
}
crea_snap && echo "Ahora podes usar  /dev/mapper/snap ..."

echo -en "\n\nEnter para undo->"; read nada
set -x
umount -f /dev/mapper/snap
dmsetup remove snap
dmsetup remove orig
losetup -d $SNAP_DEV
