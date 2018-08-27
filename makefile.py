#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2015-2018 Shenzhen Auto-link world Information Technology Co., Ltd.
  All Rights Reserved
  Name: makefile.py
  Purpose: Build all CommonAPI-Examples simplify
  Created By:    Clive Lau <liuxusheng@auto-link.com.cn>
  Created Date:  2018-03-05
  Changelog:
  Date         Desc
  2018-03-05   Created by Clive Lau
"""

# Builtin libraries
import os
import sys
import getopt
import shutil
import logging
import platform
import commands
import subprocess

# Third-party libraries

# Customized libraries


################################################################################
def usage():
    print('Usage: ' + sys.argv[0] + ' [OPTION...]\n'
          'Build all CommonAPI-Examples simplify.\n'
          '\n'
          '-h, --help' + '\t\t' + 'Give this help list\n'
          '-p, --project=NAME' + '\t' + 'Build the special project[E01HelloWorld / E02Attributes / E03Methods / E04PhoneBook / E05Manager / E06Unions / E07Mainloop]\n'
          '-V, --version' + '\t\t' + 'Print program version\n')


def is_windows_os():
    return platform.system() == 'Windows'


def get_status_output(cmd):
    output = ''
    if is_windows_os():
        try:
            status = subprocess.call(cmd)
            if not status:
                output = subprocess.check_output(cmd)
        except WindowsError:
            status = 255
            output = ''
    else:
        try:
            (status, output) = commands.getstatusoutput(cmd)
        except Exception:
            status = 255
            output = ''
    return status, output


def check_valid_tbox_device():
    status, output = get_status_output('adb devices')

    if (len(output.split()[4:]) / 2) != 1:
        return False

    status, output = get_status_output('adb shell cat /etc/tbox/device_version')
    if output.rfind('No such file or directory') != -1:
        return False

    return True


def build_and_install_project(proj):
    client = proj + 'Client'
    service = proj + 'Service'
    lib = 'lib' + proj + '-dbus.so'

    logger.debug('client:\t' + client)
    logger.debug('service:\t' + service)
    logger.debug('lib:\t' + lib)

    build_path = os.getcwd() + '/' + proj + '/build'

    if os.path.exists(build_path):
        shutil.rmtree(build_path)

    try:
        os.makedirs(build_path)
    except OSError, e:
        logger.warn(str(e))

    os.chdir(build_path)
    status, output = get_status_output('cmake ../')
    print(output)
    status, output = get_status_output('make')
    print(output)
    status, output = get_status_output('adb push ' + client + ' /usr/bin/')
    print(output)
    status, output = get_status_output('adb push ' + service + ' /usr/bin/')
    print(output)
    status, output = get_status_output('adb push ' + lib + ' /usr/lib/')
    print(output)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s/%(name)s(+ %(lineno)d): %(message)s')
    logger = logging.getLogger(__name__)

    if check_valid_tbox_device() is False:
        logger.error('Cannot detect valid TBox device')

    logger.debug('Detected valid TBox device')

    opts, args = getopt.getopt(sys.argv[1:], "hp:V", ['help', 'project=', 'version'])
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            logger.debug('help')
            usage()
            exit()
        if opt_name in ('-p', '--project'):
            build_and_install_project(opt_value)
            exit()
        if opt_name in ('-V', '--version'):
            print('Version 0.1')
            exit()
