#!/data/data/com.termux/files/usr/bin/python
"""Publica el servicio SSH como movil.local via mDNS/Zeroconf"""
import socket
import signal
import sys
from zeroconf import ServiceInfo, Zeroconf, IPVersion

def get_local_ip():
    """Obtiene la IP local del dispositivo"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

def main():
    hostname = 'movil'
    port = 8022
    ip = get_local_ip()
    
    zc = Zeroconf(ip_version=IPVersion.V4Only)
    
    # Registrar servicio SSH
    info = ServiceInfo(
        '_ssh._tcp.local.',
        f'{hostname}._ssh._tcp.local.',
        addresses=[socket.inet_aton(ip)],
        port=port,
        properties={'description': 'Termux SSH'},
        server=f'{hostname}.local.',
    )
    
    print(f'Publicando {hostname}.local -> {ip}:{port}')
    zc.register_service(info)
    
    def signal_handler(sig, frame):
        print('Deteniendo mDNS...')
        zc.unregister_service(info)
        zc.close()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Mantener corriendo
    try:
        signal.pause()
    except:
        while True:
            import time
            time.sleep(3600)

if __name__ == '__main__':
    main()
