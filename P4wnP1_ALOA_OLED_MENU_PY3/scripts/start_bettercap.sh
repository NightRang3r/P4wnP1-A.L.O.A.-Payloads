#!/bin/sh
# Wrapper to start Bettercap Web UI on a chosen port (default 8081)
PORT=${1:-8081}
HOST=127.0.0.1

# check if port is already in use
if ss -ltn "sport = :$PORT" >/dev/null 2>&1 || netstat -tulpn 2>/dev/null | grep ":$PORT" >/dev/null 2>&1; then
    echo "PORT_IN_USE"
    exit 0
fi

# try starting bettercap with common invocation patterns (caplet based)
if command -v bettercap >/dev/null 2>&1 || [ -x "/usr/local/bin/bettercap" ]; then
    BCMD=$(command -v bettercap 2>/dev/null || echo /usr/local/bin/bettercap)

    # Try several ways to run the http-ui caplet and allow the wrapper to detect the listening port
    # 1) run the named caplet
    "$BCMD" -caplet http-ui >/dev/null 2>&1 &
    sleep 0.4
    if ss -ltn "sport = :$PORT" >/dev/null 2>&1 || netstat -tulpn 2>/dev/null | grep ":$PORT" >/dev/null 2>&1; then
        echo "STARTED"
        exit 0
    fi

    # 2) run caplet file directly
    if [ -f "/usr/share/bettercap/caplets/http-ui.cap" ]; then
        "$BCMD" -caplet /usr/share/bettercap/caplets/http-ui.cap >/dev/null 2>&1 &
        sleep 0.4
        if ss -ltn "sport = :$PORT" >/dev/null 2>&1 || netstat -tulpn 2>/dev/null | grep ":$PORT" >/dev/null 2>&1; then
            echo "STARTED"
            exit 0
        fi
    fi

    # 3) try to set port via -eval then run caplet
    "$BCMD" -eval "set http-ui.port $PORT; caplets.run http-ui" >/dev/null 2>&1 &
    sleep 0.6
    if ss -ltn "sport = :$PORT" >/dev/null 2>&1 || netstat -tulpn 2>/dev/null | grep ":$PORT" >/dev/null 2>&1; then
        echo "STARTED"
        exit 0
    fi

    # 4) final attempt: run without caplet and let user configure interactively
    "$BCMD" >/dev/null 2>&1 &
    sleep 0.4
    if ss -ltn "sport = :$PORT" >/dev/null 2>&1 || netstat -tulpn 2>/dev/null | grep ":$PORT" >/dev/null 2>&1; then
        echo "STARTED"
        exit 0
    fi

    # if none of the above started a listener on the port we wanted, report failure but bettercap exists
    echo "BETTERCAP_PRESENT_NO_UI_ON_PORT"
    exit 3
fi

# no bettercap binary found
echo "NO_BETTERCAP"
exit 2
