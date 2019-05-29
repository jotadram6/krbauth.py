#!/usr/bin/env python

import subprocess
import argparse
import getpass


def krbauth(username, password):
    cmd = ['kinit', username]
    proc = subprocess.Popen(['kinit',username,'-l 2147483647'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.stdin.write(password+'\n')
    proc.stdin.flush()
    stdout, stderr = proc.communicate()
    #print stdout, stderr
    return not bool(len(stderr))

def log(message, quiet):
    if not quiet:
        print('[*] {}'.format(message))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='Kerberos username', type=str)
    parser.add_argument('-p', '--password', help='Kerberos password', type=str)
    parser.add_argument('-r', '--realm', help='Kerberos REALM', type=str)
    parser.add_argument('-q', '--quiet', help='Quiet mode', action='store_true')
    args = parser.parse_args()

    username = args.username or input('[*] Kerberos username: ')
    password = args.password or getpass.getpass('[*] Kerberos password: ')
    if args.realm:
        username = '{}@{}'.format(username, args.realm)

    log('Logging in as {}'.format(username), args.quiet)
    res = krbauth(username, password)
    if res:
        log('Succesfully Logged in!', args.quiet)
        return 0
    else:
        log('Incorrect Login!', args.quiet)
        return 1


if __name__=='__main__':
    main()
