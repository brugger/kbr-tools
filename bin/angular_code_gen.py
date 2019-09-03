#!/usr/bin/env python3
""" 
 creates the skeleton files for a module: CRUD + service + navigator.
 
 
 Kim Brugger (26 Aug 2019), contact: kim.brugger@uib.nok
"""

import sys
import os
import argparse
import subprocess
import shutil
import pprint
pp = pprint.PrettyPrinter(indent=4)

def mkdir( directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)

def make_directories( name:str) -> None:

    mkdir("src/app/{name}s".format(name=name))
    mkdir("src/app/{name}s/{name}-view".format(name=name))
    mkdir("src/app/{name}s/{name}-list".format(name=name))
    mkdir("src/app/{name}s/{name}-edit".format(name=name))
    mkdir("src/app/kbr/")
    mkdir("src/assets/")
    mkdir("src/app/kbrNotification/")


def write_file(filename:str, content:str) -> None:
    fh = open(filename, 'w')
    fh.write( content )
    fh.close()


def find_file( filename:str) -> str:
    script_dir = os.path.dirname(os.path.abspath( __file__ ))
    default_dirs = ['/usr/local/share/kbr-tools',
                    "{}/../share/".format( script_dir ),
                    '/usr/share/kbr-tools/',
                    '/usr/local/share/kbr-tools/',
                    'share/']

    for dir in default_dirs:
        full_path = "{}/{}".format( dir, filename)
        if os.path.isfile(full_path):
            return os.path.normpath(full_path)

    raise RuntimeError("File {} not found".format( filename ))


def find_dir( filename:str) -> str:
    script_dir = os.path.dirname(os.path.abspath( __file__ ))

    default_dirs = ['/usr/local/share/kbr-tools',
                    "{}/../share".format( script_dir ),
                    '/usr/share/kbr-tools/',
                    '/usr/local/share/kbr-tools/',
                    'share/']

    for dir in default_dirs:
        full_path = "{}/{}".format( dir, filename)
        if os.path.isdir(full_path):
            return os.path.normpath(full_path)

    raise RuntimeError("Dir {} not found".format( filename ))



def read_file(filename:str) -> str:
    filename = find_file( filename)
    fh = open( filename, 'r')
    content = fh.read()
    fh.close()
    return content




def make_model( name:str) -> None:
    print( 'model...')
    content = read_file("angular/template/template.model.ts")
    content = content.format(Name=name.capitalize())
    write_file("src/app/{name}s/{name}.model.ts".format(name=name), content)

    
def make_navigator( name:str ):
    print( 'navigator...')
    content = read_file("angular/template/template-navigator.ts")
    content = content.format( Name=name.capitalize(), name=name)

    write_file("src/app/{name}s/{name}-navigator.ts".format(name=name), content)



def make_service( name:str) -> None:
    print( 'service...')
    content = read_file("angular/template/template.service.ts")
    content = content.format( Name=name.capitalize(), name=name)
    write_file("src/app/{name}s/{name}.service.ts".format(name=name), content)

def launch_cmd(cmd: str, cwd: str = "") -> None:
    effective_command = cmd
    p = subprocess.Popen(effective_command, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE,
                         bufsize=1) if cwd == '' else subprocess.Popen(effective_command, stdout=subprocess.PIPE,
                                                                       shell=True, stderr=subprocess.PIPE, bufsize=1,
                                                                       cwd=cwd)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    return (p_status, stdout, stderr)


    
def make_list(name:str) -> None:

    print( 'list component...')
    launch_cmd("ng g c {name}s/{name}-list".format(name=name))

    content = read_file("angular/template/template-list/template-list.component.ts")
    content = content.format( Name=name.capitalize(), name=name)
    write_file("src/app/{name}s/{name}-list/{name}-list.component.ts".format( Name=name.capitalize(), name=name), content)


def make_view(name:str) -> None:

    print( 'view component...')
    launch_cmd("ng g c {name}s/{name}-view".format(name=name))
    content = read_file("angular/template/template-view/template-view.component.ts")
    content = content.format( Name=name.capitalize(), name=name)

    write_file("src/app/{name}s/{name}-view/{name}-view.component.ts".format( Name=name.capitalize(), name=name), content)



def make_edit(name:str) -> None:

    print( 'edit component...')
    launch_cmd("ng g c {name}s/{name}-edit".format(name=name))
    content = read_file("angular/template/template-edit/template-edit.component.ts")
    content = content.format( Name=name.capitalize(), name=name)
    write_file("src/app/{name}s/{name}-edit/{name}-edit.component.ts".format( Name=name.capitalize(), name=name), content)


def make_kbrNotification() -> None:

    print( 'kbrNotification component...')
    launch_cmd("ng g c kbrNotification/confirmation --module app")
    shutil.copy( find_file( 'angular/kbrNotification/confirmation/confirmation.component.ts'),'src/app/kbrNotification/confirmation/')
    shutil.copy( find_file( 'angular/kbrNotification/confirmation/confirmation.component.html'),'src/app/kbrNotification/confirmation/')
    shutil.copy( find_file( 'angular/kbrNotification/kbrNotification.ts'),'src/app/kbrNotification/')

def copy_kbr_library() -> None:
    print( 'kbr library...')
    src = 'angular/kbr/'
    src = find_dir( src )
    dst = 'src/app/kbr/'
    src_files = os.listdir( src )
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile( dst+file_name):
            continue
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dst)

    shutil.copy( find_file( 'angular/assets/kbr.css'),'src/assets/')
    launch_cmd("ng g m routing --flat --module=app")

    shutil.copy( find_file( 'angular/routing.module.ts'),'src/app/')



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='angular module creator (CRUD + Navigator + service)')

    parser.add_argument("-b", "--base", default=False, action='store_true', help="install core library and components.")
    parser.add_argument("-m", "--module",  help="name of module to create CRUD for")



    args = parser.parse_args()
 
    if ( args.base):
        print('installing base system')
        copy_kbr_library()
        make_kbrNotification()

    if (args.module):
        name = args.module[ 0 ].lower()
        print( "Creating skeleton files for module: {name}".format( name=name ) )
        make_directories( name )
        make_navigator( name )
        make_service( name )
        make_model( name )
        make_view(name )
        make_list(name )
        make_edit(name )
