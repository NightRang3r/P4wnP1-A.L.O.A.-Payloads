#!/bin/sh
# Wrapper to start Bettercap Web UI on a chosen port (default 8081)
PORT=${1:-8081}
HOST=127.0.0.1

# check if port is already in use
if ss -ltn "sport = :$PORT" >/dev/null 2>&1 || netstat -tulpn 2>/dev/null | grep ":$PORT" >/dev/null 2>&1; then
    echo "PORT_IN_USE"
    exit 0
fi

# try starting bettercap
if command -v bettercap >/dev/null 2>&1; then
    # newer bettercap supports --http-ui and --http-ui-port
    bettercap --http-ui --http-ui-port $PORT >/dev/null 2>&1 &
    echo "STARTED"
    exit 0
fi

# fallback: look for bettercap installed in /usr/local/bin
if [ -x "/usr/local/bin/bettercap" ]; then
    /usr/local/bin/bettercap --http-ui --http-ui-port $PORT >/dev/null 2>&1 &
    echo "STARTED"
    exit 0
fi

# no bettercap found
echo "NO_BETTERCAP"
exit 2
