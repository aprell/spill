#!/bin/sh

if [ "$(which moon)" = "" ]; then
	echo "No moon found in PATH"
	echo "Make sure to have Lua installed and try"
	echo ""
	echo "    luarocks install moonscript"
	echo ""
	echo "Until then..."
	exit 2
fi

moon main.moon "$@"
