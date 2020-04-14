#!/bin/bash
cd /home/pi/Desktop/WRO2/
name=wro
if [[ -e $name.log ]] ; then
	i=1
	while [[ -e $name-$i.log ]] ; do
		let i++
	done
	mv $name.log $name-$i.log
fi
/usr/bin/python3 /home/pi/Desktop/WRO2/wro.py >> /home/pi/Desktop/WRO2/$name.log