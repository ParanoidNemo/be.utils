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
import os, sys
import argparse
import logging
import tempfile
import shutil
import tarfile
import cmd

#Import custom module(s)
import check        #temp solution, have to change it when create __init__.py in spam
import beshell      #temp solution, have to change it when create __init__.py in spam
import archive      #temp solution, have to change it when create __init__.py in spam

#create log messages
logging.basicConfig(filename='be.utils.log', level=logging.DEBUG)

#create parser for script argument(s)
#parser = argparse.ArgumentParser()
#parser.add_argument('-b', '--backup', type=argparse.FileType(), action='store_true', help='Create a backup of an existing theme and configuration')
#parser.add_argument('-u', '--update', action='store_true', help='Check if there are any update to BE::Shell project')
#parser.add_argument('-i', '--install', action='store_true', help='Install theme(s), configuration(s) and extra feature(s)')
#parser.add_argument('-t', '--theme', help='Install only a new theme')
#parser.add_argument('-l', '--local', help='Check for theme(s) locally')
#parser.add_argument('-r', '--remote', help='Check for theme(s) on remote git repo')
#parser.add_argument('-d', '--directory', default='~/project/be-shell', help='BE::Shell local project directory')
#args = parser.parse_args()

class Interactive(cmd.Cmd):
    intro = "Welcome to the interactive shell for be.utils.\nPlease tipe help o ? to see a list of possible commands.\n"
    prompt = '>> '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.namespace = {}

    def do_quit(self, line):
        """Close the program"""
        print("\nThanks to have used be.utils")
        sys.exit(1)

    def do_EOF(self, line):
        """With CTR-D close the program"""
        self.do_quit(line)

    do_q = do_quit

    def do_install(self, line):
        """Check if BE::Shell is installed on your system, and if not install it"""
        if check.prg('be.shell'):
            print('BE::Shell is already installed, nothing to do.')
        else:
            beshell.install()

    def do_update(self, line):
        """Check if there are some updates for BE::Shell, and if there are proceed to install them"""
        if check.prg('be.shell'):
            print('BE::Shell is correctly installed, checking update(s)..')
            print('Searching for local be.shell git repo..')
            if -l in sys.argv:
                check.dir(directory)        #should work, have to test it
                print('Check for update')
                beshell.up()
            else:
                print('Check for update')
                beshell.up
        else:
            print("BE::Shell isn't installed, you want to install it? [yes/no]")
            if input() == "yes":
                beshell.install()
            elif input() == "no":
                print(KeyboardInterrupt('Installation aborted by user, nothing to do.'))

    def do_backup(self, line):
        """Check if there are an existing configuration and create a backup if there are one"""
        def backup():
            if os.path.isfile(os.path.join(Configuration.config_dir, 'be.shell')):
                print('Found existing configuration.\nDo you want to back it up? [yes/no]')
                if input() == 'yes':
                    bk_path = os.path.expanduser('~/.local/share/be.shell/backup/')
#-------------------------------------------------------------------------------
#--------------------------TUTTO DA RICONTROLLARE-------------------------------
#-------------------------------------------------------------------------------
                    tempfile.mkdtemp(dir=bk_path)
                    for path, dirs, file in os.walk(bk_path):
                        _dir = dirs[0]
                        dirs.clear()
                        if _dir.startswith('tmp'):
                            tmp_dir = _dir
                            archive.compress(tmp_dir, bk_path, name=beshell.Theme.name)
                            os.chdir(bk_path)
                            tarfile.TarFile.add(beshell.Configuration.config_dir, arcname=beshell.Theme.name)
                            os.removedirs(_dir)
                            #il ciclo for assegna correttamente tmp_dir, ma genera errore, capire perché,
                    print('Everything done correctly. To restore your backup launch the script with the xxx flag')
                else:
                    raise KeyboardInterrupt('Backup aborted by user, nothing to do.')
            else:
                print('No existing configuration found, nothing to do')

    def precmd(self, line):
        """Execute actions before running the command"""
        self.raw_line = line
        try:
            return(line.format_map(self.namespace))
        except KeyError as ex:
            print("The command %s isn't defined" %ex)
        except ValueError:
            print("The input cannot be a number")

        return ''

    def help_default(self):
        print(self.default.__doc__)

if __name__ == '__main__':
    bul = Interactive()
    bul.cmdloop()
