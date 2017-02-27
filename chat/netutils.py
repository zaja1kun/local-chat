import netifaces as ni


def get_ifaces_info():
    interfaces = {}
    for interface in ni.interfaces():
        try:
            interfaces[interface] = ni.ifaddresses(interface)[ni.AF_INET][0]
        except KeyError:
            pass
    return interfaces
