# termux-mdns

mDNS publisher and resolver for Termux (Android).

Publishes `movil.local` on the local network via Zeroconf so other machines can find the phone by hostname instead of dynamic DHCP IPs.

## Components

| Script | Purpose |
|--------|---------|
| `mdns-publish.py` | Publishes `movil.local:8022` as an SSH service via mDNS/Zeroconf |
| `mdns-resolve` | Resolves `.local` hostnames via raw UDP multicast (RFC 6762) |
| `ssh-mdns-proxy` | SSH ProxyCommand with mDNS → Tailscale → cache fallback chain |

## Install

```bash
pkg install python
pip install zeroconf
./install.sh
```

## Usage

From any machine on the LAN:
```bash
ssh -p 8022 movil.local
```

From the phone to other machines:
```bash
ssh dell   # resolves via mdns-resolve → ssh-mdns-proxy
```

## Boot

The installer adds `mdns-publish.py` to `~/.termux/boot/start-services` so it starts automatically when Termux boots.

## License

MIT
