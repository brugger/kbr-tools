import re

import kbr.file_utils as file_utils
import kbr.json_utils as json_utils

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
    version_file = file_utils.find_first( 'version.json')
    if version_file is not None:
        version = json_utils.read( version_file )
        major, minor, patch = bumping( bump, version['major'], version['minor'], version['patch'] )
        version[ 'major' ] = major
        version[ 'minor' ] = minor
        version[ 'patch' ] = patch
        json_utils.write( version_file, version )
        info(mesg="Version after bump ")
        return

    version_file = file_utils.find_first( 'setup.ts')
    if version_file is not None:
        major, minor, patch  = get_ts_version(version_file)
        major, minor, patch = bumping( bump, major, minor, patch )
        set_ts_version(version_file, major, minor, patch)
        info(mesg="Version after bump ")
        return


    raise RuntimeError('Could not find version file')


def get_ts_version(filename:str) -> []:
    data = file_utils.readin_file( filename )
    match = re.search(r"version: '(\d+)\.(\d+).(\d+)'", data, re.MULTILINE)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))

    raise RuntimeError( "Could not find version string in {}".format(filename))



def set_ts_version(filename:str, major:int, minor:int, patch:int) -> []:
    data = file_utils.readin_file( filename )
    version = "version: '{}.{}.{}'".format( major, minor, patch)
    data = re.sub(r"version: '(.*)'", version, data, re.MULTILINE)
    file_utils.write( filename, data)





def _pretty_print( major:int, minor:int, patch:int, mesg:str="Version: " ) -> None:
    print( "{}{}.{}.{}".format( mesg, major, minor, patch))


def info(mesg:str="Version: ") -> None:
    version_file = file_utils.find_first( 'version.json')
    if version_file is not None:
        info = json_utils.read( version_file )
        _pretty_print( info['major'], info['minor'], info['patch'], mesg=mesg)
        return

    version_file = file_utils.find_first( 'setup.ts')
    if version_file is not None:
        version = get_ts_version(version_file)
        major, minor, patch = get_ts_version( version_file )
        _pretty_print( major, minor, patch, mesg=mesg)
        return


def set(version:str) -> None:
    major, minor, patch = map( int, version.split('.'))

    info(mesg="Version before bump ")
    version_file = file_utils.find_first( 'version.json')
    if version_file is not None:
        version = json_utils.read( version_file )
        version[ 'major' ] = major
        version[ 'minor' ] = minor
        version[ 'patch' ] = patch
        json_utils.write( version_file, version )
        info(mesg="Version after bump ")
        return

    version_file = file_utils.find_first( 'setup.ts')
    if version_file is not None:
        set_ts_version(version_file, major, minor, patch)
        info(mesg="Version after bump ")
        return

    raise RuntimeError('Could not find version file')

