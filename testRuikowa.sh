if test -n $1
then
	bash INSTALL.sh
fi

cd   tests/Ruikowa/Lang


bash Lisp/testLisp.sh
