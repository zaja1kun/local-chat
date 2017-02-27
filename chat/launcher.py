#!/usr/bin/env python3
import logging
import argparse
import urwid

from chat.cli.interface import ChatInterface
from chat.cli.dialog import CheckListDialog
from chat import netutils


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s')
LOG = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser(
        description='Simple pure python LAN chat')
    args = parser.parse_args()
    return args


def main():
    args = _parse_args()
    interfaces = netutils.get_ifaces_info()
    exit_code, iface = CheckListDialog(
        'Choose interface', 15, 40, interfaces.keys()).show()
    if exit_code != 0:
        return
    chat = ChatInterface()
    chat.add_message('System', 'Starting local chat using `%s` interface. Your '
                     'IP address is `%s`' % (iface, interfaces[iface]['addr']))
    chat.run()


if __name__ == '__main__':
    main()
