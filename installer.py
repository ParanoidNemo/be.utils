#!/usr/bin/env python

#   Copyright (C) 2015 by Andrea Calzavacca <paranoid.nemo@gmail.com>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the
#   Free Software Foundation, Inc.,
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

#Import std library module(s)
import os.path
import io
import sys
import argparse
import logging

#Import custom module(s)
from . import check     #temp solution, have to change it when create __init__.py in spam
from . import beshell   #temp solution, have to change it when create __init__.py in spam

#create log messages NEED TO SET IT CORRECTLY
#logging.basicConfig(filename='be.installer.log',level=logging.DEBUG)
#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')

#create parser for script argument(s)
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--backup', type=argparse.FileType(), action='store_true', help='Create a backup of an existing theme and configuration')
parser.add_argument('-u', '--update', action='store_true', help='Check if there are any update to BE::Shell project')
parser.add_argument('-i', '--install', action='store_true', help='Install theme(s), configuration(s) and extra feature(s)')
#parser.add_argument('-t', '--theme', help='Install only a new theme')
#parser.add_argument('-l', '--local', help='Check for theme(s) locally')
#parser.add_argument('-r', '--remote', help='Check for theme(s) on remote git repo')
parser.add_argument('-d', '--directory', default='~/project/be-shell', help='BE::Shell local project directory')
args = parser.parse_args()

#start define function(s)
def update():
    if check.prg('be.shell'):
        print('BE::Shell is correctly installed, checking update(s)..')
        print('Searching for local be.shell git repo..')
        check.dir(directory)        #should work, have to test it
        print('Check for update')
        beshell.up()
    else:
        print("BE::Shell isn't installed, you want to install it? [yes/no]")
        if input() == "yes":
            beshell.install()
        elif input() == "no":
            raise KeyboardInterrupt('Installation aborted by user, nothing to do.')
            sys.exit(1)

def install():
    if check.prg('be.shell'):
        print('BE::Shell is already installed, nothing to do.')
        sys.exit(1)
    else:
        beshell.install()

def backup(_path):
    if os.path.isfile(os.path.expanduser(config_dir()['config'] + 'be.shell')):
        print('Found existing configuration.\nDo you want to back it up? [yes/no]')
        if input() == 'yes':
            pass        #find how to create tar archive with given file(s) and folder(s)
        else:
            raise KeyboardInterrupt('Backup aborted by user, nothing to do.')
            sys.exit(1)
