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
import cmd

#Import downloaded module(s)
import git

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
    intro = "Welcome to the interactive shell for be.utils.\nPlease tipe 'help' o '?' to see a list of possible commands.\n"
    prompt = '--> '
    ruler = '-'
    doc_header = "Documented commands - type 'help <topics>' to visualize the specific help"
    #misc_header = ''

    #define init sequence
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.namespace = {}

    #define std behavior
    def emptyline(self):
        """Do nothing if the line is empty"""
        pass

    def default(self, line):
        """Define what to do with not expected commands"""
        try:
            if not line.isnumeric():
                print("The input command doesn't exists. Type 'help' for a list of defined command")
            else:
                print('Error: Input must be a string')
        except Exception as ex:
            logging.debug('Line: ', line)
            logging.debug('Message: %s\n', ex)
            print(ex)

    #defining escape commands and sequences
    def do_quit(self, line):
        """Close the program"""
        print("\nThanks to have used be.utils")
        sys.exit(1)

    def do_EOF(self, line):
        """With CTR-D close the program"""
        self.do_quit(line)

    #defining functions
    def do_install(self, line):
        """Check if BE::Shell is installed on your system, and if not install it"""
        if check.prg('be.shell'):
            print('BE::Shell is already installed, nothing to do.')
        else:
            beshell.install()

    def do_update(self, line):
        """Check if there are some updates for BE::Shell, and if there are proceed to install them"""
        if check.prg('be.shell'):
            print('BE::Shell is correctly installed, checking update(s)..\nSearching for local be.shell git repo..\nCheck for updates')
            beshell.up()
        else:
            print("BE::Shell isn't installed, you want to install it? [yes/no]")
            if input() == "yes":
                beshell.install()
            elif input() == "no":
                print('Installation aborted by user, nothing to do.')

    def do_backup(self, line):
        """Check if there are an existing configuration and create a backup if there are one"""
        if os.path.isfile(os.path.join(beshell.Configuration.config_dir(), 'be.shell')):
            print('Found existing configuration.\nDo you want to back it up? [yes/no]')
            if input() == 'yes':
                beshell.backup()
            else:
                print('Backup aborted by user, nothing to do.')
        else:
            print('No existing configuration found, nothing to do')

    def do_list(self, line):
        """Print the locally installed themes, and the avaiable ones"""
        print('\n---Installed themes---')
        if beshell.Theme.l_list('list') == '':
            print('None')
        else:
            pass
        print('\n---Avaiable themes---')
        beshell.Theme.d_list('list')

    def do_download(self, line):
        """Download themes and features for BE::Shell from git Bedevil repo"""
        def devil():
            try:
                os.makedirs(os.path.join(beshell.project_dir, 'Bedevil'))
            except FileExistsError:
                pass
            except Exception:
                logging.debug('Line: ', line)
                logging.debug('Message: %s\n', ex)
                print(ex)

            _local = os.path.expanduser('~/project/Bedevil')
            _remote = 'https://github.com/Bedevil/be.shell.git'
            g = git.cmd.Git(_local)

            if not os.path.isdir(os.path.join(_local, 'be.shell')):
                try:
                    os.chdir(_local)
                    print('Start cloning git repo..\n')
                    g.clone(_remote, 'be.shell')
                    print('Everything done without errors')
                except FileNotFoundError as ex:
                    logging.debug('Line: ', line)
                    logging.debug('Message: %s\n', ex)
                    print(ex)
            else:
                ctrl_seq = 'Already up-to-date.'
                g2 = git.cmd.Git(os.path.join(_local, 'be.shell'))
                print('Local repository already exists, searching for updates..\n..')
                git_out = g2.pull('--recurse-submodule')
                o = git_out.split(sep='\n')

                if o[-1:][0] == ctrl_seq:
                    print(o[-1:][0])
                else:
                    print('Repository updated')

        devil()

#    def do_restore(self, line):
#        """Restore a theme previusly backuped"""
#        bk_path = os.path.expanduser('~/.local/share/be.shell/backup')
#        a = {}
#        i = 0
#        for index, file in enumerate(os.listdir(bk_path)):
#            print(index, '-->', file)
#            a[i] = file
#            i += 1
#        print("Choose which backup you want to restore")
#        c = input()
#        try:
#            _c = int(c)
#            if _c in a:
#                if os.path.isfile(beshell.Configuration.main_file()):
#                    print("Another theme are already installed, you want to backup it [yes/no]? ")
#                    if input() == 'yes':
#                        beshell.backup()
#                    elif input() == 'no':
#                        print('Warning:\nThe actual config will be overwrite. Are you sure [yes/no]? ')
#                        if input() == 'yes':
#                            archive.extract(, bk_path, a[_c])

    def do_themeinstall(self, line):
        """Install a BE::Shell theme locally downloaded. See also 'list' for a list of already downloaded themes"""
        d = beshell.Theme.d_list()
        l = beshell.Theme.l_list()
        _d = []
        _l = []
        _o = []
        i = 0
        a = {}
        for item in d.values():
            _d.append(item)
        for item in l.values():
            _l.append(item)
        for _d[i] in _l:
            if True:
                pass
            else:
                try:
                    _o.append(_d[i])
                except Exception:
                    pass
        for index, item in enumerate(_o):
            print(index, '-->', item)
        print("Choose which theme you want to install: ")
        c = input()
        try:
            _c = int(c)
            if _c in a:
                if os.path.isfile(beshell.Configuration.main_file()):
                    print("Another theme are already installed, you want to backup it [yes/no]? ")
                    if input() == 'yes':
                        beshell.backup()
                    elif input() == 'no':
                        print('Warning:\nThe actual config will be overwrite. Are you sure [yes/no]? ')
                        if input() == 'yes':
                            os.chdir(beshell.Configuration.config_dir())
                            os.remove(beshell.Configuration.main_file())
                            config_file = os.path.join(beshell.project_dir, 'Bedevil', 'be.shell', 'Config', a[_c] + '.conf')
                            shutil.copy2(config_file, beshell.Configuration.config_dir())
                            os.rename(config_file, 'be.shell')
                            print("Configuration file copied..\n")
                            theme_dir = os.path.join(beshell.project_dir, 'Bedevil', 'be.shell', 'Themes', a[_c])
                            shutil.copytree(theme_dir, os.path.join(beshell.Configuration.main_dir, 'Themes'))
                            print("Theme directory copied..\nPlease reload the shell to see the applied theme")
                        elif input() == 'no':
                            print('Operation aborted by user.\nNothing to do')
                else:
                    os.chdir(beshell.Configuration.config_dir())
                    config_file = os.path.join(beshell.project_dir, 'Bedevil', 'be.shell', 'Config', a[_c] + '.conf')
                    shutil.copy2(config_file, beshell.Configuration.config_dir())
                    os.rename(config_file, 'be.shell')
                    print("Configuration file copied..\n")
                    theme_dir = os.path.join(beshell.project_dir, 'Bedevil', 'be.shell', 'Themes', a[_c])
                    shutil.copytree(theme_dir, os.path.join(beshell.Configuration.main_dir, 'Themes'))
                    print("Theme directory copied..\nPlease reload the shell to see the applied theme")
            else:
                _i = []
                for index, item in enumerate(a.keys()):
                    _i.append(str(index))
                print('\nYou have to choose a number between', _i[0], 'and', _i[-1])

        except ValueError:
            print('\n------\nError:\nInput must be an int')
        except Exception as ex:
            logging.debug('Line: ', line)
            logging.debug('Message: %s\n', ex)
            print(ex)

    def do_apply(self, line):
        """Apply a theme already installed. See also 'list' command for a list of installed themes"""
        d = beshell.Theme.l_list()
        beshell.Theme.l_list('dict')
        print("Choose which theme you want to apply:\n")
        c = input()
        try:
            _c = int(c)
            if _c in d:
        #-----------------------------------------------------------------------
        #-----------------------TRY TESTATO FINO A QUI--------------------------
        #-----------------------------------------------------------------------
                if os.path.isfile(beshell.Configuration.main_file()):
                    print("Another theme are already installed, you want to backup it [yes/no]? ")
                    if input() == 'yes':
                        beshell.backup()
                    elif input() == 'no':
                        print('Warning:\nThe actual config will be overwrite. Are you sure [yes/no]? ')
                        if input() == 'yes':
                            os.chdir(beshell.Configuration.config_dir())
                            os.remove(beshell.Configuration.main_file())
                            config_file = beshell.Configuration.main_file + '.' + d[_c]
                            os.rename(config_file, 'be.shell')
                            print('Everything done without errors.\nPlease reload the shell to use the applied theme')
                        elif input() == 'no':
                            print('Operation aborted by user.\nNothing to do')
                else:
                    os.chdir(beshell.Configuration.config_dir())
                    config_file = beshell.Configuration.main_file + '.' + d[_c]
                    os.rename(config_file, 'be.shell')
                    print('Everything done without errors.\nPlease reload the shell to use the applied theme')
            else:
                i = []
                for index, item in enumerate(d.keys()):
                    i.append(str(index))
                print('\nYou have to choose a number between', i[0], 'and', i[-1])

        except ValueError:
            print('\n------\nError:\nInput must be an int')
        except Exception as ex:
            logging.debug('Line: ', line)
            logging.debug('Message: %s\n', ex)
            print(ex)

    #define shotcurt sequences
#    do_i = do_install
#    do_u = do_update
#    do_b = do_backup
#    do_l = do_list
#    do_q = do_quit
#    do_d = do_download
#    do_a = do_apply
#    do_t = do_themeinstall

    #define help alternative function(s)
    def help_default(self):
        print(self.default.__doc__)

if __name__ == '__main__':
    bul = Interactive()
    if len(sys.argv) > 1:
        bul.onecmd(' '.join(sys.argv[1:]))
    else:
        bul.cmdloop()
