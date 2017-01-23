""""
Description           : This module check the answer and report the
                        attacker computer.
                        the students must get a COMPILED version of this file.
Author                : Ori Levi and Dana Even-Haim
FileName              : check_answer.py
Date                  : 18.01.2017
Version               : 1.0
"""

import socket
import webbrowser


class IncorrectAnswerError(Exception):
    pass


def check_answer(answer, attacker_ip, attacker_port):
    """
    check your answer and open it if correct.
    send status to the attacker server.

    if the answer is incorrect raise IncorrectAnswerError

    :param answer: the answer you think.
    :type answer: int

    :param attacker_ip: the ip of the attacker computer
    :type attacker_ip: str

    :param attacker_port: the port of the attacker computer
    :type attacker_port: int
    """

    if answer != 61:
        raise IncorrectAnswerError()

    url = 'http://www.up2me.co.il/images/31048619.png'
    webbrowser.open(url, new=1)

    # send to server
    s = socket.socket()
    s.connect((attacker_ip, attacker_port))
    while True:
        s.send('done')

        s.settimeout(2)
        try:
            data = s.recv(1024)
            if data and data == 'done':
                break
        except socket.timeout:
            pass
