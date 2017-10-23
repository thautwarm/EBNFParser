if test -z $1
then
	cd   tests/Ruikowa/Lang/Cm
	bash testCm.sh
else
	bash INSTALL.sh
	cd   tests/Ruikowa/Lang/Cm
	bash testCm.sh
fi
