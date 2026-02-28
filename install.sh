#!/data/data/com.termux/files/usr/bin/bash
set -e

BIN="$HOME/.local/bin"
BOOT="$HOME/.termux/boot/start-services"

mkdir -p "$BIN"

cp mdns-publish.py mdns-resolve ssh-mdns-proxy "$BIN/"
chmod +x "$BIN/mdns-publish.py" "$BIN/mdns-resolve" "$BIN/ssh-mdns-proxy"

# Add to boot if not already there
if ! grep -q "mdns-publish" "$BOOT" 2>/dev/null; then
    sed -i "/^sshd$/a \\\n# Iniciar mDNS (publica movil.local)\nnohup python ~/.local/bin/mdns-publish.py > /dev/null 2>&1 &" "$BOOT"
    echo "Added mdns-publish to boot script"
fi

# Start if not running
if ! pgrep -f mdns-publish.py > /dev/null; then
    nohup python "$BIN/mdns-publish.py" > /dev/null 2>&1 &
    echo "mdns-publish started (PID: $!)"
else
    echo "mdns-publish already running"
fi

echo "Install complete"
