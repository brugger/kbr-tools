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

def write_file(filename:str, content:str) -> None:
    fh = open(filename, 'w')
    fh.write( content )
    fh.close()

def write_template_to_file(infile:str, outfile:str, name:str) -> None:
    content = read_file(infile)
    content = content.format( Name=name.capitalize(), name=name)
    write_file(outfile.format(name=name), content)

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


def launch_cmd(cmd: str, cwd: str = "") -> None:
    effective_command = cmd
    p = subprocess.Popen(effective_command, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE,
                         bufsize=1) if cwd == '' else subprocess.Popen(effective_command, stdout=subprocess.PIPE,
                                                                       shell=True, stderr=subprocess.PIPE, bufsize=1,
                                                                       cwd=cwd)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    if stderr:
        print( stderr )
    return (p_status, stdout, stderr)



def make_model( name:str) -> None:
    print( 'model...')
    write_template_to_file("angular/template/template.model.ts",
                           "src/app/{name}s/{name}.model.ts",
                           name)
    return

    
def make_navigator( name:str ):
    print( 'navigator...')
    write_template_to_file("angular/template/template-navigator.ts",
                           "src/app/{name}s/{name}-navigator.ts",
                           name)



def make_service( name:str) -> None:
    print( 'service...')
    write_template_to_file("angular/template/template.service.ts",
                           "src/app/{name}s/{name}.service.ts",
                           name)



    
def make_list(name:str) -> None:

    print( 'list component...')
    launch_cmd("ng g c {name}s/{name}-list --module app".format(name=name))

    write_template_to_file("angular/template/template-list/template-list.component.ts",
                           "src/app/{name}s/{name}-list/{name}-list.component.ts",
                           name)
    write_template_to_file("angular/template/template-list/template-list.component.html",
                           "src/app/{name}s/{name}-list/{name}-list.component.html",
                           name)


def make_view(name:str) -> None:

    print( 'view component...')

    launch_cmd("ng g c {name}s/{name}-view --module app".format(name=name))
    write_template_to_file("angular/template/template-view/template-view.component.ts",
                           "src/app/{name}s/{name}-view/{name}-view.component.ts",
                           name)
    write_template_to_file("angular/template/template-view/template-view.component.html",
                           "src/app/{name}s/{name}-view/{name}-view.component.html",
                           name)


def make_edit(name:str) -> None:

    print( 'edit component...')
    launch_cmd("ng g c {name}s/{name}-edit --module app".format(name=name))
    write_template_to_file("angular/template/template-edit/template-edit.component.ts",
                           "src/app/{name}s/{name}-edit/{name}-edit.component.ts",
                           name)
    write_template_to_file("angular/template/template-edit/template-edit.component.html",
                           "src/app/{name}s/{name}-edit/{name}-edit.component.html",
                           name)


def make_kbrNotification() -> None:

    print( 'kbrNotification component...')
    launch_cmd("ng g c kbrNotification/confirmation --module app")
    launch_cmd("ng g c kbrNotification/single-input --module app")

    src = 'angular/kbrNotification/'
    src = find_dir( src )
    dst = 'src/app/kbrNotification/'
    src_files = os.listdir( src )
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile( dst+file_name):
            os.remove( dst+file_name) 

        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dst)



#    shutil.copy( find_file( 'angular/kbrNotification/confirmation/confirmation.component.ts'),'src/app/kbrNotification/confirmation/')
#    shutil.copy( find_file( 'angular/kbrNotification/confirmation/confirmation.component.html'),'src/app/kbrNotification/confirmation/')
#    shutil.copy( find_file( 'angular/kbrNotification/kbrNotification.ts'),'src/app/kbrNotification/')

def copy_kbr_library() -> None:
    print( 'kbr library...')
    mkdir("src/app/kbr/")
    mkdir("src/assets/")
    mkdir("src/app/kbrNotification/")

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


def make_auth() -> None:

    print( 'Auth components...')
    launch_cmd("ng g c auth/login --module app")
    launch_cmd("ng g c auth/logout --module app")

    shutil.copy( find_file( 'angular/auth/login/login.component.ts'),'src/app/auth/login/')
    shutil.copy( find_file( 'angular/auth/logout/logout.component.ts'),'src/app/auth/logout/')


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='angular module creator (CRUD + Navigator + service)')

    parser.add_argument("-b", "--base", default=False, action='store_true', help="install core library and components.")
    parser.add_argument("-f", "--force", default=False, action='store_true', help="will overwrite existing files")

    parser.add_argument("-m", "--module",  help="name of module to create CRUD for")



    args = parser.parse_args()
 
    if ( args.base):
        print('installing base system')
        copy_kbr_library()
        make_kbrNotification()
        make_auth( )

    if (args.module):
        name = args.module.lower()
        print( "Creating skeleton files for module: {name}".format( name=name ) )
        make_directories( name )
        make_navigator( name )
        make_service( name )
        make_model( name )
        make_view(name )
        make_list(name )
        make_edit(name )

        print( "Add the following routes to routing.ts")
        print("  {{ path: '{name}s/:id',           component: {Name}ListComponent}},".format(Name=name.capitalize(), name=name))
        print("  {{ path: '{name}s',           component: {Name}ListComponent}},".format(Name=name.capitalize(), name=name))
