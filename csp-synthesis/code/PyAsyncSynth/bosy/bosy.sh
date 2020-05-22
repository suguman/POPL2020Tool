#!/usr/bin/env bash

#swift run -c release BoSy ${@:1}
#swift run --skip-build -c release BoSy ${@:1}
echo "exec: swift run --build-path $1 -c release BoSy ${@:2}"
swift run --build-path $1 -c release BoSy ${@:2}

exit_code=$?

# Terminate all tools that may have been started by BoSy
for f in Tools/*; do
    if [ ! -f $f ]; then
        continue
    fi
    tool=$(basename $f)
    killall $tool &> /dev/null
done

exit $?
