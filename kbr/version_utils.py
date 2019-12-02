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
        version = json_version( version_file )
        major, miror, patch = bumping( bump, version['major'], version['minor'], version['patch'] )
        version[ 'major' ] = major
        version[ 'minor' ] = minor
        version[ 'patch' ] = patch
        return

    raise RuntimeError('Could not find version file')


def _pretty_print( major:int, minor:int, patch:int, mesg:str="Version: " ) -> None:
    print( "{}{}.{}.{}".format( mesg, major, minor, patch))


def info(mesg:str="Version: ") -> None:
    version_file = file_utils.find_first( 'version.json')
    if version_file is not None:
        info = json_utils.read( version_file )
        _pretty_print( info['major'], info['minor'], info['patch'], mesg=mesg)
        return


def set(version:str) -> None:
    return None
