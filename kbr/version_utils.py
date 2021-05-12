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


def bumping( bump:str, major:int, minor:int, patch:int, dev:int=0, rc:int=0 ) -> []:
    if bump == 'major':
        return [major+1, 0, 0, 0,0]
    elif bump == 'minor':
        return [major, minor+1, 0, 0,0]
    elif bump == 'patch':
        return [major, minor, patch+1, 0,0]
    elif bump == 'dev':
        return [ major, minor, patch, dev+1,0]
    elif bump == 'rc':
        return [ major, minor, patch, 0, rc+1]


    else:
        raise RuntimeError("Unkown bump {}".format( bump ))

def bump_version(bump:str) -> None:

    info(mesg="Version before bump ")
    version_file = find_version_file( VERSION_FILE )
    if version_file is not None:
        version = json_utils.read( version_file )
        if 'dev' not in version:
            version['dev'] = 0
        if 'rc' not in version:
            version['rc'] = 0
        major, minor, patch, dev, rc = bumping( bump, version['major'], version['minor'], version['patch'], version['dev'], version['rc'] )
        version[ 'major' ] = major
        version[ 'minor' ] = minor
        version[ 'patch' ] = patch
        version[ 'dev' ] = dev
        version[ 'rc' ] = rc
        if not version['dev']:
            del version['dev']
        if not version['rc']:
            del version['rc']
        json_utils.write( version_file, version )
        info(mesg="Version after bump ")
        return

    version_file = find_version_file( ANGULAR_SETUP )
    if version_file is not None:
        major, minor, patch  = get_ts_version(version_file)
        major, minor, patch, _ = bumping( bump, major, minor, patch )
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


def info(mesg:str="Version: ") -> None:
    v_string = as_string()
    print(f"{mesg}{v_string}")



def find_version_file(name:str, path:str=".") -> str:
    filename = file_utils.find_first(name, path)
    if filename is None:
        filename = file_utils.find_updir(name, path)

    return filename

def as_string(module_name:str=None):

    if module_name is not None:
        try:
            return module_version(module_name)
        except:
            pass

    version_file = find_version_file( VERSION_FILE )
    if version_file is not None:
        info = json_utils.read( version_file )
        if 'dev' in info and info['dev']:
            return  "{}.{}.{}-dev{}".format( info['major'], info['minor'], info['patch'], info['dev'])
        elif 'rc' in info and info['rc']:
            return  "{}.{}.{}-rc{}".format( info['major'], info['minor'], info['patch'], info['rc'])
        else:
            return  "{}.{}.{}".format( info['major'], info['minor'], info['patch'])

    version_file = find_version_file( ANGULAR_SETUP )
    if version_file is not None:
        major, minor, patch = get_ts_version( version_file )
        return  "{}.{}.{}".format(major, minor, patch)

    raise FileNotFoundError("version file '{}' or '{}' not found".format( VERSION_FILE, ANGULAR_SETUP))


def changed():
    version_file = find_version_file( VERSION_FILE )
    if version_file is not None:
        return file_utils.changed( version_file)

    version_file = find_version_file( ANGULAR_SETUP )
    if version_file is not None:
        return file_utils.changed( version_file)

    raise FileNotFoundError("version file '{}' or '{}' not found".format( VERSION_FILE, ANGULAR_SETUP))



def set(version:str) -> None:
    major, minor, patch = map( int, version.split('.'))

    info(mesg="Version before bump ")
    version_file = find_version_file( VERSION_FILE )
    if version_file is not None:
        version = json_utils.read( version_file )
        version[ 'major' ] = major
        version[ 'minor' ] = minor
        version[ 'patch' ] = patch
        json_utils.write( version_file, version )
        info(mesg="Version after bump ")
        return

    version_file = find_version_file( ANGULAR_SETUP )
    if version_file is not None:
        set_ts_version(version_file, major, minor, patch)
        info(mesg="Version after bump ")
        return

    raise RuntimeError('Could not find version file')


def tag( release_file:str=None):
    cmd = "git tag "
    if release_file is not None:
        cmd += " -F {}".format( release_file)
    else:
        cmd += " -m 'tagged version {}'".format( as_string())

    cmd += " {} ".format( as_string() )

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


def write_version_json_file():
    if not os.path.isfile( VERSION_FILE ):
        json_utils.write( VERSION_FILE, {'major':0, 'minor': 0, 'patch':0} )

def init_python_env():

    dirs = ['bin', 'docs', 't']
    for dir in dirs:
        if not os.path.isdir( dir ):
            os.mkdir(dir)

    if not os.path.isfile( VERSION_FILE ):
        json_utils.write( VERSION_FILE, {'major':0, 'minor': 0, 'patch':0} )

#    if not os.path.isfile( UPDATES_FILE ):
#        write_update_file()


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
    release_file = RELEASE_FILE.format( as_string())
    tag( release_file )
