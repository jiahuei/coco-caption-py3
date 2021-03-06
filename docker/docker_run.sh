#!/usr/bin/env bash

SCRIPT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker run -it \
    --gpus all \
    -v "${SCRIPT_ROOT}/..:/src" \
    -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY="$DISPLAY" \
    -u "$(id -u)":"$(id -g)" \
    --rm jiahuei/python27:java8 bash /src/run.sh
