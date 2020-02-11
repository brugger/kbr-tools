import re
import os
import sys
import shutil

import kbr.json_utils as json_utils
import kbr.run_utils  as run_utils
import kbr.file_utils as file_utils

VERSION_FILE = "version.json"
ANGULAR_SETUP = "setup.ts"
UPDATES_FILE = "updates.md"
RELEASE_FILE = "docs/release-{}.md"



def _bump_major( major:int, minor:int, patch:int ) -> []:

    major += 1
    minor = 0
    patch = 0

    return [major, minor, patch]


def _bump_minor( major:int, minor:int, patch:int ) -> []:

    minor += 1
    patch  = 0

    return [major, minor, patch]

def _bump_patch( major:int, minor:int, patch:int ) -> []:

    patch += 1

    return [major, minor, patch]


def bumping( bump:str, major:int, minor:int, patch:int ) -> []:
    if bump == 'major':
        return _bump_major( major, minor, patch)
    elif bump == 'minor':
        return _bump_minor( major, minor, patch)
    elif bump == 'patch':
        return _bump_patch( major, minor, patch)

    else:
        raise RuntimeError("Unkown bump {}".format( bump ))

def bump_version(bump:str) -> None:

    info(mesg="Version before bump ")
    version_file = file_utils.find_first( VERSION_FILE )
    if version_file is not None:
        version = json_utils.read( version_file )
        major, minor, patch = bumping( bump, version['major'], version['minor'], version['patch'] )
        version[ 'major' ] = major
        version[ 'minor' ] = minor
        version[ 'patch' ] = patch
        json_utils.write( version_file, version )
        info(mesg="Version after bump ")
        return

    version_file = file_utils.find_first( ANGULAR_SETUP )
    if version_file is not None:
        major, minor, patch  = get_ts_version(version_file)
        major, minor, patch = bumping( bump, major, minor, patch )
        set_ts_version(version_file, major, minor, patch)
        info(mesg="Version after bump ")
        return


    raise RuntimeError('Could not find version file')


def get_ts_version(filename:str) -> []:
    data = file_utils.read(filename)
    match = re.search(r"version: '(\d+)\.(\d+).(\d+)'", data, re.MULTILINE)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))

    raise RuntimeError( "Could not find version string in {}".format(filename))


def set_ts_version(filename:str, major:int, minor:int, patch:int) -> []:
    data = file_utils.read(filename)
    version = "version: '{}.{}.{}'".format( major, minor, patch)
    data = re.sub(r"version: '(.*)'", version, data, re.MULTILINE)
    file_utils.write( filename, data)

def _pretty_print( major:int, minor:int, patch:int, mesg:str="Version: " ) -> None:
    print( "{}{}.{}.{}".format( mesg, major, minor, patch))


def info(mesg:str="Version: ") -> None:
    version_file = file_utils.find_first( VERSION_FILE )
    if version_file is not None:
        info = json_utils.read( version_file )
        _pretty_print( info['major'], info['minor'], info['patch'], mesg=mesg)
        return

    version_file = file_utils.find_first( ANGULAR_SETUP )
    if version_file is not None:
        major, minor, patch = get_ts_version( version_file )
        _pretty_print( major, minor, patch, mesg=mesg)
        return

    raise FileNotFoundError("version file '{}' or '{}' not found".format( VERSION_FILE, ANGULAR_SETUP))



def as_string():
    version_file = file_utils.find_first( VERSION_FILE )
    if version_file is not None:
        info = json_utils.read( version_file )
        return  "{}.{}.{}".format( info['major'], info['minor'], info['patch'])

    version_file = file_utils.find_first( ANGULAR_SETUP )
    if version_file is not None:
        major, minor, patch = get_ts_version( version_file )
        return  "{}.{}.{}".format(major, minor, patch)

    raise FileNotFoundError("version file '{}' or '{}' not found".format( VERSION_FILE, ANGULAR_SETUP))


def set(version:str) -> None:
    major, minor, patch = map( int, version.split('.'))

    info(mesg="Version before bump ")
    version_file = file_utils.find_first( VERSION_FILE )
    if version_file is not None:
        version = json_utils.read( version_file )
        version[ 'major' ] = major
        version[ 'minor' ] = minor
        version[ 'patch' ] = patch
        json_utils.write( version_file, version )
        info(mesg="Version after bump ")
        return

    version_file = file_utils.find_first( ANGULAR_SETUP )
    if version_file is not None:
        set_ts_version(version_file, major, minor, patch)
        info(mesg="Version after bump ")
        return

    raise RuntimeError('Could not find version file')


def tag( release_file:str=None):
    cmd = "git tag "
    if release_file is not None:
        cmd += " -F {}".format( release_file)
    cmd += " {} master".format( as_string() )

    #print( cmd )
    run_utils.launch_cmd( cmd )
    cmd = "git push --tags"
    #print( cmd )
    run_utils.launch_cmd( cmd )



def module_version( module_name) -> str:
    import pkg_resources
    return pkg_resources.get_distribution( module_name ).version


def write_update_file():
    if os.path.isfile( UPDATES_FILE ):
        raise RuntimeError("{} already exists".format( UPDATES_FILE ))

    content = '''Major Changes
###

Minor Changes
###

Patches
###
'''
    file_utils.write( UPDATES_FILE, content )

def release_prep():

    release_filename = RELEASE_FILE.format( as_string() )

    if os.path.isfile( release_filename):
        print( "Release file ({}) already exists!".format( release_filename))
        sys.exit( -1 )


    shutil.move(UPDATES_FILE, release_filename )
    write_update_file()

def init_python_env():

    dirs = ['bin', 'docs', 't']
    for dir in dirs:
        if not os.path.isdir( dir ):
            os.mkdir(dir)

    if not os.path.isfile( VERSION_FILE ):
        json_utils.write( VERSION_FILE, {'major':0, 'minor': 0, 'patch':0} )

    if not os.path.isfile( UPDATES_FILE ):
        write_update_file()


def _git_tags() -> []:
    info = run_utils.launch_cmd("git tags -l")
    tags = info.stdout.decode('utf-8')
    return tags


def release_info(version:str=None):
    if version is None:
        tags = _git_tags().split("\n")[::-1]
        print( "\n".join( tags)  , end="")

        version = tags[ -2 ]

    release_file = RELEASE_FILE.format( version )

    if os.path.isfile( release_file ):
        print( "\nRelease notes for {}\n=============\n".format( version ))
        data = file_utils.read( release_file )
        print( data )
    else:
        print("No release file found for version {}".format( version ))


def release_push():
    return None


def release_push():
    release_file = RELEASE_FILE.format( as_string())
    tag( release_file )
