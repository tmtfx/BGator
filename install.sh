#!/bin/bash
echo "This will download and install feedparser to your system, continue? (type y or n)"
read text
if [ $text == "y" ]
then
echo
pkgman install feedparser_python
ret3=$?
echo
else
	echo "Proceeding..."
	ret3=1
fi
echo "Now checking for Bethon.tar.gz presence"
if [ -e Bethon.tar.gz ]
then
	tar -xf Bethon.tar.gz
	cd Bethon
	make && make install
	ret2=$?
	cd ..
else
	echo "Bethon.tar.gz not present in this folder..."
	echo "Do you wish to git clone Bethon to your system? (type y or n)"
	read text
	if [ $text == "y" ]
	then
	git clone https://github.com/tmtfx/Bethon
	cd Bethon
	make && make install
	ret2=$?
	cd ..
	else
	echo "Proceeding..."
	ret2=1
	fi
fi
echo
if [ -e BGator.py ]
then
	mkdir /boot/home/config/non-packaged/data/BGator
	cp BGator.py /boot/home/config/non-packaged/data/BGator
	ret4=$?
	ln -s /boot/home/config/non-packaged/data/BGator/BGator.py /boot/home/config/non-packaged/bin/BGator
	mkdir /boot/home/config/settings/deskbar/menu/Applications/
	ln -s /boot/home/config/non-packaged/bin/BGator /boot/home/config/settings/deskbar/menu/Applications/BGator
	ret5=$?
else
	echo Main program missing
	ret4=1
	ret5=1
fi
echo
DIRECTORY=`pwd`/help
if [ -d $DIRECTORY  ]
then
	cp -R help /boot/home/config/non-packaged/data/BGator
	ret6=$?
else
	echo Missing help directory and images
	ret6=1
fi
echo


if [ $ret2 -lt 1 ]
then
	echo Installation of Bethon OK
else
	echo Installation of Bethon FAILED
fi
if [ $ret3 -lt 1 ]
then
	echo Installation of feedparser OK
else
	echo Installation of feedparser FAILED
fi
if [ $ret4 -lt 1 ] 
then
        echo Installation of BGator OK
else
        echo Installation of BGator FAILED
fi
if [ $ret5 -lt 1 ]
then
        echo Installation of menu entry OK
else
        echo Installation of menu entry FAILED
fi

if [ $ret6 -lt 1 ]
then
        echo Installation of help and images OK
else
        echo Installation of help and images FAILED
fi
