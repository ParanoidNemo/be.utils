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
from spam import check
from spam import beshell

#create log messages NEED TO SET IT CORRECTLY
logging.basicConfig(filename='be.installer.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

#create parser for script argument(s)
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--backup', type=argparse.FileType(), help='Create a backup of an existing theme and configuration')
parser.add_argument('-u', '--update', help='Check if there are any update to BE::Shell project')
parser.add_argument('-i', '--install', help='Install theme(s), configuration(s) and extra feature(s)')
parser.add_argument('-t', '--theme', help='Install only a new theme')
parser.add_argument('-l', '--local', help='Check for theme(s) locally')
parser.add_argument('-r', '--remote', help='Check for theme(s) on remote git repo')
parser.add_argument('-d', '--directory', default='~/project/be-shell', help='BE::Shell local project directory')
args = parser.parse_args()

#start define function(s)
def update():
    if check.prg('be.shell'):
        print('BE::Shell is correctly installed, checking update(s)..')
        print('Searching for local be.shell git repo..')
        check.dir('')#find how to use the -d arg for that
        print('Check for update')
        beshell.up()
    else:
        print("BE::Shell isn't installed, you want to install it? [yes/no]")
        confirm = input()
        if confirm == "yes":
            beshell.install()
        elif confirm == "no":
            raise KeyboardInterrupt('Installation aborted by user, nothing to do.')
