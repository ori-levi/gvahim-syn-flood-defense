""""
Description           : This simple server should run on any student's computer.
                        run this server with arguments, must done before the
                        attack begin, it's also register the student to the
                        table.
Author                : Ori Levi and Dana Even-Haim
FileName              : simple_server.py
Date                  : 18.01.2017
Version               : 1.0
"""

import socket
import argparse
import threading

from contextlib import closing


def get_my_ip():
    """
    Get the ip of the computer
    :return: The ip of the running computer.
    :rtype: str
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


def notify_my_ip(attacker_ip, attacker_port, name):
    with closing(socket.socket(socket.AF_INET)) as client:
        client.connect((attacker_ip, attacker_port))

        msg = '{}-{}'.format(name, get_my_ip())
        while True:
            client.send(msg)

            client.settimeout(2)
            try:
                data = client.recv(1024)
                if data and data == 'done':
                    break
            except socket.timeout:
                pass


def target(_, addr):
    """
    dummy target for the thread
    DO NOTHING
    :param _:
    :param addr:
    :return:
    """
    print 'Handling %s' % addr
    while True:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--attacker-ip', help='The attacker ip',
                        required=True)
    parser.add_argument('-p', '--attacker-port', help='The attacket port',
                        required=True, type=int)
    parser.add_argument('-n', '--name', help='Your name', required=True)

    args = parser.parse_args()
    notify_my_ip(args.attacker_ip, args.attacker_port, args.name)

    with closing(socket.socket()) as server:
        server.bind(('0.0.0.0', 5057))
        server.listen(1)

        try:
            while True:
                cs, ca = server.accept()
                threading.Thread(target=target, args=(cs, ca)).start()
        except KeyboardInterrupt:
            pass
