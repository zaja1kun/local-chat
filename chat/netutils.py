import netifaces as ni
import socket
import threading
from threading import Thread
from select import select
import pickle

from chat import constants as const


def get_ifaces_info():
    interfaces = {}
    for interface in ni.interfaces():
        try:
            interface_info = ni.ifaddresses(interface)[ni.AF_INET][0]
            if 'broadcast' in interface_info:
                interfaces[interface] = interface_info
        except KeyError:
            pass
    return interfaces


class BroadcastClient:
    def __init__(self, interface, callback, port=const.CHAT_PORT):
        self.interface = interface
        self.ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
        self.broadcast_ip = ni.ifaddresses(interface)[ni.AF_INET][0]['broadcast']
        self.port = port
        self.callback = callback

        self._sock = self._open_broadcast_socket()
        self._stop_event = threading.Event()
        self._consuming_thread = Thread(target=self._blocking_consume,
                                        name='CommunicationThread')

    def _open_broadcast_socket(self, port=const.CHAT_PORT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((self.broadcast_ip, port))
        return sock

    def start(self):
        """Start thread for blocking message consuming."""
        self._stop_event.clear()
        self._consuming_thread.start()

    def stop(self):
        """Stop thread for blocking message consuming."""
        self._stop_event.set()
        self._consuming_thread.join()

    def _blocking_consume(self):
        while not self._stop_event.is_set():
            readable, *_ = select(
                (self._sock, ), tuple(), tuple(), const.RECV_TIMEOUT)
            if readable:
                bin_message, (sender, _) = self._sock.recvfrom(self.port)
                if sender == self.ip:
                    continue
                message = pickle.loads(bin_message)
                self.callback(sender, message)

    def send_msg(self, message):
        bin_message = pickle.dumps(message)
        self._sock.sendto(bin_message, (self.broadcast_ip, self.port))

    def close(self):
        self._sock.close()
