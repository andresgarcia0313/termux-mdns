# termux-mdns

mDNS publisher and resolver for Termux (Android).

## Problem

Android phones get dynamic IPs via DHCP. Every time the phone reconnects to WiFi, the IP changes. This makes SSH connections unreliable since you'd need to find the new IP each time.

## Solution

This project publishes `movil.local` on the local network via Zeroconf (mDNS), so any machine on the LAN can find the phone by hostname regardless of its current IP.

It also includes a resolver and SSH proxy so the phone can find other `.local` machines on the network.

## Components

| Script | What it does |
|--------|-------------|
| `mdns-publish.py` | Publishes `movil.local:8022` as an SSH service via mDNS multicast |
| `mdns-resolve` | Resolves `.local` hostnames via raw UDP multicast (RFC 6762) |
| `ssh-mdns-proxy` | SSH ProxyCommand with fallback chain: mDNS → Tailscale DNS → local cache |

## Requirements

- [Termux](https://termux.dev) with [Termux:Boot](https://wiki.termux.com/wiki/Termux:Boot) (for auto-start)
- Python 3
- `zeroconf` Python package
- `sshd` running in Termux (default port 8022)

## Install

```bash
pkg install python openssh
pip install zeroconf
git clone https://github.com/andresgarcia0313/termux-mdns.git
cd termux-mdns
./install.sh
```

The installer copies scripts to `~/.local/bin/`, adds `mdns-publish.py` to `~/.termux/boot/start-services`, and starts the service immediately.

## Usage

### From another machine → phone

```bash
# Direct (any machine with mDNS/avahi support)
ssh -p 8022 user@movil.local

# Or add to ~/.ssh/config:
Host phone
    HostName movil.local
    Port 8022
    User u0_a260
```

### From the phone → other machines

```bash
# Uses ssh-mdns-proxy as ProxyCommand
ssh dell          # resolves dell-latitude3400.local via mDNS
ssh lenovo        # resolves lenovo-ideapad.local via mDNS
```

To use the proxy, add this to your `~/.ssh/config` on the phone:

```
Host dell lenovo
    ProxyCommand ~/.local/bin/ssh-mdns-proxy %h %p
```

## How it works

1. **Publishing:** `mdns-publish.py` uses the `zeroconf` library to register an `_ssh._tcp` service on the mDNS multicast group (224.0.0.251:5353). Any device on the LAN with mDNS support (Linux/avahi, macOS/Bonjour, Windows) can resolve `movil.local`.

2. **Resolving:** `mdns-resolve` sends raw UDP queries to the mDNS multicast address and parses A record responses. This works without needing avahi (which isn't available in Termux).

3. **SSH proxy:** `ssh-mdns-proxy` chains three resolution methods — mDNS first, then Tailscale DNS, then a local IP cache — so SSH connections work across different network conditions.

## License

MIT
