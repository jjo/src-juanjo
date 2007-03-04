#!/bin/bash
# insertion-sort.bash.sh: Insertion sort implementation in bash
#                         Heavy use of bash array features: slicing, merging, etc
#
# Author: JuanJo Ciarlante <jjo@irrigacion.gov.ar>
# License: GPLv2
#
# Test with:   ./insertion-sort.bash.sh -t
#
: ${DEBUG:=1}  # debug, override with:  DEBUG=1 ./scriptname ..

# Global array: "list"
typeset -a list
# Load whitespace separated numbers from just stdin 1st line
if [ "$1" = "-t" ];then
	read -a list < <(od -An -w32 -t u2 /dev/urandom )
else
	read -a list
fi
numelem=${#list[*]}

# Shows the list, marking the element whose index es $1 by surrounding it with
# the two chars passed as $2; whole line prefixed with $3
showlist() { echo "$3"${list[@]:0:$1} ${2:0:1}${list[$1]}${2:1:1} ${list[@]:$1+1}; }

# loop "pivot" from 2nd elem, to end of list
for((i=1;i<numelem;i++))do
	((DEBUG))&&showlist i "[]" " "
	# From current "pivot", back to 1st elem
	for((j=i;j;j--))do
		# search for the 1st elem less than current "pivot" ...
		[[ "${list[j-1]}" -le "${list[i]}" ]] && break
	done
	((i==j)) && continue ## no insertion was needed for this element
	# ... move list[i] (pivot) to the left of list[j]:
	list=(${list[@]:0:j} ${list[i]} ${list[j]} ${list[@]:j+1:i-(j+1)} ${list[@]:i+1})
	#         {0,j-1}       {i}       {j}        {j+1,i-1}              {i+1,last}
	((DEBUG))&&showlist j "<>" "*"
done
echo $'Result:\n'${list[@]}
