#!/usr/bin/env python3
import logging
import argparse

from chat.client import ChatClient


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
    chat = ChatClient()
    chat.run()


if __name__ == '__main__':
    main()
